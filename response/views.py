from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import os, json, datetime, random

from .models import TimeTable, Query
from .tools.misc import *

from timetable.settings import BASE_DIR
from shinyang import SHINYANG, this_year, this_semester

OPTIONS = ['지금', '어제', '오늘', '내일', '월', '화', '수',
           '목', '금', '월요일', '화요일', '수요일', '목요일', '금요일']

def keyboard(request):
    return JsonResponse({
        'type': 'buttons',
        'buttons': ['도움말', '바로검색']
    })

def helper():
    with open(os.path.join(BASE_DIR, 'response/etc/helper.txt')) as f:
        text = f.read()
    return text

def view_period_time(dt):
    tmp = TimeTable.objects.filter(date=dt).first()
    if not tmp:
        return error('no_class_today', now=dt)
    grade, division = tmp.grade, tmp.division
    rows = TimeTable.objects.filter(
        date=dt, grade=grade, division=division).order_by('period')
    m = '시정표({}):'.format(format_date(dt))
    for row in rows:
        m += ('\n{}교시 '.format(row.period) + period_time(row))
    return m

def view_period_time_wrapper(content, now):
    contents = [c.strip() for c in content.split()]
    if len(contents) == 1:
        text = view_period_time(now)
    else:
        opts = OPTIONS.copy()
        opts.remove('지금')
        # more than two options -- e.g., 시정표 내일 금요일
        # or wrong input options
        if len(contents) > 2 or contents[1] not in opts:
            text = error('wrong_input')
        else:
            date = weekday_tuner(now, contents[1])
            text = view_period_time(date)
    return text


def view_class_weekday(grade, division, dt):
    assert (grade, division) in SHINYANG[this_year][this_semester]['GRADE_DIVISION']
    wd_kor = weekday(dt)
    rows = TimeTable.objects.filter(
        grade=grade, division=division, date=dt).order_by('period')
    if rows.count() == 0:
        return error('no_class_today', now=dt)
    title = '{}학년 {}반\n{}({}요일):'.format(grade, division, format_date(dt), wd_kor)
    l = [class_period(row.period, row.subject, row.teacher) for row in rows]
    message = '\n'.join(l)
    return '\n'.join([title, message])


def view_teacher_weekday(teacher, dt):
    # ! teacher list should be in SHINYANG[this_year]
    validate_teacher(teacher)
    all_periods = TimeTable.objects.filter(
        teacher__contains=teacher, date=dt).order_by('period')
    if all_periods.count() == 0:
        return error('no_class_today_teacher', teacher=teacher, now=dt)
    last_period = all_periods.last().period
    wd_kor = weekday(dt)
    rows = list()
    for i in range(1, last_period + 1):
        try:
            row = all_periods.get(period=i)
            rows.append('{}교시 {} {}-{}'.format(i, row.subject, row.grade, row.division))
        except:
            rows.append('{}교시 -'.format(i))
    message = '\n'.join(rows)
    title = '{}\n{}({}요일):'.format(teacher, format_date(dt), wd_kor)
    return '\n'.join([title, message])


def view_class_now(grade, division, dt):
    if dt.weekday() >= 5:
        return error('weekend')
    assert (grade, division) in SHINYANG[this_year][this_semester]['GRADE_DIVISION']
    if dt.time() < datetime.time(9, 15):
        message = late_night_message()
        return random.choice(message)
    row = TimeTable.objects.filter(
        grade=grade, division=division, date=dt, start__lt=dt).order_by('-period').first()
    if not row:
        return error('no_class_today', now=dt)
    period = row.period
    title = '{}\n{}학년 {}반({}교시):\n{}'.format(
        format_date(dt), grade, division, period, period_time(row))
    if dt.time() > row.end:
        message = error('no_class_now')
        title = '\n'.join([message, title])
    return '\n'.join([title, row.subject, row.teacher])


def view_teacher_now(teacher, dt):
    # ! teacher list should be in SHINYANG[this_year]
    validate_teacher(teacher)
    if dt.weekday() >= 5:
        return error('weekend')
    if dt.time() < datetime.time(9, 15):
        message = late_night_message(dt)
        return random.choice(message)
    rows = TimeTable.objects.filter(teacher__contains=teacher, date=dt)
    if rows.count() == 0:
        return error('no_class_today_teacher', now=dt, teacher=teacher)
    else:
        # 오늘 수업이 있긴 함
        try:
            row = rows.filter(start__lt=dt).order_by('-period')[0]
            name = '{}\n{}({}교시):\n{}'.format(format_date(
                dt), row.teacher, row.period, period_time(row))
            teachingDivision = '{}학년 {}반 {}'.format(
                row.grade, row.division, row.subject)

            if dt.time() > row.end:
                message = error('no_class_now')
                name = '{}\n{}'.format(message, name)
            return '{}\n{}'.format(name, teachingDivision)
        except:
            period = rows.order_by('period')[0].period
            return error('not_yet', now=dt, teacher=teacher, period=period)


def view_class(target, now, datetime):
    grade, division = [int(elem.strip()) for elem in target.split('-')]
    if now:
        return view_class_now(grade, division, datetime)
    else:
        return view_class_weekday(grade, division, datetime)


def view_teacher(target, now, datetime):
    if now:
        return view_teacher_now(target, datetime)
    else:
        return view_teacher_weekday(target, datetime)


@csrf_exempt
def answer(request):
    now = datetime.datetime.now()
    try:
        input_request = request.body.decode('utf-8')
        input_json = json.loads(input_request)
        content = input_json['content'].strip()
        q_option = {'option': content}
    except:
        text = error(404)
    else:
        quick_options = {
            '도움말': helper(),
            '지금': now.strftime('%Y-%m-%d %H:%M'),
            '오늘': '{} {}요일'.format(now.date(), weekday(now)),
            '바로검색': '키보드 작동중'
        }
        if content in quick_options.keys():
            text = quick_options[content]
        elif '시정표' in content:
            text = view_period_time_wrapper(content, now)
        else:
            try:
                # determine if an option exists
                contents = content.split(maxsplit=1)
                # no option
                if len(contents) == 1:
                    target = content
                    params = {'target': target, 'now': False, 'datetime': now}
                # option exists
                else:
                    target, option = contents
                    if option not in OPTIONS:
                        raise ValueError
                    if option == '지금':
                        params = {'target': target, 'now': True, 'datetime': now}
                    # searching for weekday
                    else:
                        date = weekday_tuner(now, contents[1])
                        params = {'target': target, 'now': False, 'datetime': date}
                text = view_class(**params) if '-' in target else view_teacher(**params)
            except:
                text = error('wrong_input')
    finally:
        Query.objects.create(option=q_option.get('option', '-'))
        return JsonResponse({'message': {'text': text}})