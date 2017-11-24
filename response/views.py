from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

def keyboard(request):
	return JsonResponse({
		"type": "buttons",
		"buttons": ["도움말", "바로검색"]
	})

import os
import json
import datetime
import random

from .models import TimeTable, Query
from .tools.misc import weekday, weekday_rev, late_night_message, validate_teacher, period_time, format_date, error, message_title, class_period, weekday_tuner

from timetable.settings import BASE_DIR
from shinyang import SHINYANG, this_year, this_semester

OPTIONS = ['지금', '어제', '오늘', '내일', '월', '화', '수', '목', '금', '월요일', '화요일', '수요일', '목요일', '금요일']


def view_class_weekday(grade, division, dt):
	assert (grade, division) in SHINYANG[this_year][this_semester]["GRADE_DIVISION"]
	wd = weekday(dt)
	rows = TimeTable.objects.filter(grade=grade, division=division, date=dt).order_by("period")
	if rows.count() == 0:
		return error('no_class_today', now=dt)
	title = "{}학년 {}반\n{}({}요일):".format(grade, division, format_date(dt), wd)
	l = [class_period(row.period, row.subject, row.teacher) for row in rows]
	message = '\n'.join(l)
	return '\n'.join([title, message])

def view_teacher_weekday(teacher, dt):
	validate_teacher(teacher) #! teacher list should be in SHINYANG[this_year]
	all_periods = TimeTable.objects.filter(teacher__contains=teacher, date=dt).order_by("period")
	if all_periods.count() == 0:
		return error('no_class_today_teacher', teacher=teacher, now=dt)
	periods = all_periods.last().period
	wd = weekday(dt)
	rows = list()
	for i in range(periods):
		try:
			row = all_periods.get(period=(i+1))
			rows.append("{}교시 {} {}-{}".format(i+1, row.subject, row.grade, row.division))
		except:
			rows.append("{}교시 -".format(i+1))
	message = '\n'.join(rows)
	title = "{}\n{}({}요일):".format(teacher, format_date(dt), wd)
	return "\n".join([title,message])

def view_class_now(grade, division, dt):
	if dt.weekday() >= 5:
		return error('weekend')
	assert (grade, division) in SHINYANG[this_year][this_semester]["GRADE_DIVISION"]
	if dt.time() < datetime.time(9,15):
		message = late_night_message()
		return random.choice(message)
	row = TimeTable.objects.filter(grade=grade, division=division, date=dt, start__lt=dt).order_by("-period").first()
	if not row:
		return error('no_class_today', now=dt)
	period = row.period
	title = "{}\n{}학년 {}반({}교시):\n{}".format(format_date(dt), grade, division, period, period_time(row))
	if dt.time() > row.end:
		message = error('no_class_now')
		title = '\n'.join([message, title])
	return '\n'.join([title,row.subject,row.teacher])

def view_teacher_now(teacher, dt):
	validate_teacher(teacher) #! teacher list should be in SHINYANG[this_year]
	if dt.weekday() >= 5:
		return error('weekend')
	if dt.time() < datetime.time(9,15):
		message = late_night_message(dt)
		return random.choice(message)
	rows = TimeTable.objects.filter(teacher__contains=teacher, date=dt)
	if rows.count() == 0:
		return error('no_class_today_teacher', now=dt, teacher=teacher)
	else:
		# 오늘 수업이 있긴 함
		try:
			row = rows.filter(start__lt=dt).order_by("-period")[0]
			name = "{}\n{}({}교시):\n{}".format(format_date(dt), row.teacher, row.period, period_time(row))
			teachingDivision = "{}학년 {}반 {}".format(row.grade, row.division, row.subject)

			if dt.time() > row.end:
				message = error('no_class_now')
				name = "{}\n{}".format(message, name)
			return "{}\n{}".format(name,teachingDivision)
		except:
			period = rows.order_by("period")[0].period
			return error('not_yet', now=dt, teacher=teacher, period=period)


def view_class(target, options):
	dt = options['datetime']
	grade, division = [int(elem.strip()) for elem in target.split('-')]
	if options["now"]:
		return view_class_now(grade, division, dt)
	else:
		return view_class_weekday(grade, division, dt)

def view_teacher(target, options):
	dt = options['datetime']
	if options["now"]:
		return view_teacher_now(target, dt)
	else:
		return view_teacher_weekday(target, dt)


@csrf_exempt
def answer(request):
	now = datetime.datetime.now()
	try:
		input_request = request.body.decode("utf-8")
		input_json = json.loads(input_request)
		content = input_json["content"].strip()
	except:
                q_option = None
		text = error(404)

	# message processed
	else:
		q_option = {'option': content} # overwrite later
		if content == "도움말":
			with open(os.path.join(BASE_DIR, "response/etc/helper.txt")) as f:
				text = f.read()
		elif content == "지금":
			text = now.strftime("%Y-%m-%d %H:%M")
		elif content == "오늘":
			text = "{} {}요일".format(now.date(), weekday(now))
		elif "검색" in content:
			text = "키보드 작동중"
		elif "시정표" in content:
			contents = [c.strip() for c in content.split()]
			if len(contents) == 1:
				q_option = {'option': content}
				text = view_period_time(now)
			else:
				opts = OPTIONS.copy()
				opts.remove('지금')
				if len(contents) > 2 or contents[1] not in opts:
					text = error('wrong_input')
				else:
					q_option = {'option': contents[1]}
					d = weekday_tuner(now, contents[1])
					text = view_period_time(d)

		else:
			try:
				# determine if an option exists
				contents = content.split(' ', 1)
				# there's no option
				if len(contents) == 1:
					target = content
					if len(target.split("-")) > 1:
						q_option = {'grade_division': target}
						# Query.objects.create(grade_division=target)
						text = view_class(target, {"now": False, "datetime": now})
					else:
						q_option = {'teacher': target}
						# Query.objects.create(teacher=target)
						text = view_teacher(target, {"now": False, "datetime": now})

				# option exists
				else:
					option = contents[1].strip()
					if option not in OPTIONS:
						raise

					target = contents[0]
					if option == "지금":
						if len(target.split("-")) > 1:
							q_option = {'grade_division': target, 'option': option}
							text = view_class(target, {"now": True, "datetime": now})
						else:
							# teacher now
							q_option = {'teacher': target, 'option': option}
							text = view_teacher(target, {"now": True, "datetime": now})
					# searching for weekday
					else:
						d = weekday_tuner(now, contents[1])
						if len(target.split("-")) > 1:
							q_option = {'grade_division': target, 'option': contents[1]}
							text = view_class(target, {"now": False, "datetime": d})
						else:
							q_option = {'teacher': target, 'option': contents[1]}
							# searching for teacher weekday
							text = view_teacher(target, {"now": False, "datetime": d})
			except:
				text = error('wrong_input')
	finally:
        if q_option != None:
        	Query.objects.create(**q_option)
		return JsonResponse({"message": {"text": text}})


def view_period_time(dt):
	tmp = TimeTable.objects.filter(date=dt).first()
	if not tmp:
		return error('no_class_today', now=dt)
	grade, division = tmp.grade, tmp.division
	rows = TimeTable.objects.filter(date=dt, grade=grade, division=division).order_by("period")
	m = "시정표({}):".format(format_date(dt))
	for row in rows:
		m += ('\n{}교시 '.format(row.period) + period_time(row))
	return m
