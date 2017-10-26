# 해야할 일:
# 1. 시정표/시간표 변경 적용
# 시정표 변경 인터페이스: 해당 요일 기본 시간표를 해당 날짜로 복사하는 함수. => 날짜를 입력하면 해당 날짜의 시정표가 준대로 변경.
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

from .models import TimeTable
from .tools.timetablemod import Modifier
from .tools.misc import weekday, late_night_message, validate_teacher

from timetable.settings import BASE_DIR
from grade_division import GRADE_DIVISION

now = datetime.datetime.now()
today = weekday()


# 1학년 1반(오늘):
# 1교시 국어
# 2교시 수학
# 3교시 사회
# 4교시 영어
# 5교시 역사
# 6교시 체육
# 7교시 -
def view_class_weekday(grade, division, weekday):
	assert (grade, division) in GRADE_DIVISION
	try:
		periods = 7

		rows = TimeTable.objects.filter(grade=grade, division=division, weekday=weekday).order_by("period")
		assert len(rows) > 0
		l = list()
		for i in range(periods):
			try:
				l.append("{}교시 {}".format(i+1, rows[i].subject))
			except:
				l.append("{}교시 -".format(i+1))
		name = "{}학년 {}반({}요일):".format(grade, division, weekday)
		return JsonResponse({
			"message": {"text": ("{}\n"*7 + "{}").format(name, l[0], l[1], l[2], l[3], l[4], l[5], l[6])}})
	except:
		return JsonResponse({
			"message": {"text": "오늘은 수업이 없습니다."}})



# 선생님(오늘):
# 1교시 1-1
# 2교시 -
# 3교시 -
# 4교시 2-2
# 5교시 2-3
# 6교시 -
# 7교시 -
def view_teacher_weekday(teacher, weekday):
	assert validate_teacher(teacher)
	try:
		assert len(TimeTable.objects.filter(teacher=teacher, weekday=weekday)) > 0
	except:
		return JsonResponse({
		"message": {"text": "{}선생님은 오늘 수업이 없습니다.".format(teacher)}})
	periods = 7
	r = list()
	for i in range(periods):
		try:
			row = TimeTable.objects.get(teacher=teacher, period=(i+1), weekday=weekday)
			r.append("{}교시 {} {}-{}".format(i+1, row.subject, row.grade, row.division))
		except:
			r.append("{}교시 -".format(i+1))
	name = "{}({}요일):".format(teacher, weekday)
	return JsonResponse({
			"message": {"text": ("{}\n"*7 + "{}").format(name,r[0],r[1],r[2],r[3],r[4],r[5],r[6])}})


# 1학년 1반(4교시):
# 국어
# 선생님
# 교실
def view_class_now(grade, division, t=now):
	assert (grade, division) in GRADE_DIVISION
	try:
		if t.time() < datetime.time(9,00):
			message = late_night_message()
			return JsonResponse({
				"message": {"text": message[random.randint(0, len(message)-1)]}})

		row = TimeTable.objects.filter(grade=grade, division=division, weekday=today, start__lt=t).order_by("-period")[0]
		period = row.period
		name = "{}학년 {}반({}교시):".format(grade, division, period)

		if t.time() > row.end:
			message = "지금은 수업중이 아닙니다.\n<최근 수업>"
			name = "{}\n{}".format(message, name)
		return JsonResponse({
				"message": {"text": "{}\n{}\n{}".format(name,row.subject,row.teacher)}})
	except:
		return JsonResponse({
				"message": {"text": "오늘은 수업이 없습니다."}})



# 선생님(4교시):
# 교실
# 1학년 1반
def view_teacher_now(teacher, t=now):
	assert validate_teacher(teacher)
	if t.time() < datetime.time(9,00):
		message = late_night_message()
		if t.time() < datetime.time(6,00):
			message.append("집에서 주무시고 계신데 왜요?(꺄아)")
		return JsonResponse({
			"message": {"text": message[random.randint(0, len(message)-1)]}})
	try:
		rows = TimeTable.objects.filter(teacher=teacher, weekday=today)
		assert len(rows) > 0
	except:
		return JsonResponse({
			"message": {"text": "{}선생님은 오늘 수업이 없습니다.".format(teacher)}})
	else:
		# 오늘 수업이 있긴 함
		try:
			row = rows.filter(start__lt=t).order_by("-period")[0]
			name = "{}({}교시):".format(row.teacher, row.period)
			teachingDivision = "{}학년 {}반 {}".format(row.grade, row.division, row.subject)

			if t.time() > row.end:
				message = "지금은 수업중이 아닙니다.\n<최근 수업>"
				name = "{}\n{}".format(message, name)
			return JsonResponse({
				"message": {"text": "{}\n{}".format(name,teachingDivision)}})
		except:
			period = rows.order_by("period")[0].period
			return JsonResponse({
				"message": {"text": "오늘 {}선생님의 첫 수업은 {}교시부터입니다.".format(teacher, period)}})


def view_class(target, options):
	grade, division = map(int, map(str.strip, target.split("-")))
	try:
		if options["now"]:
			return view_class_now(grade, division)
		else:
			return view_class_weekday(grade, division, options["weekday"])
	except:
		return JsonResponse({
			"message": {"text": "학년과 반이 올바르지 않습니다."}})

def view_teacher(target, options):
	try:
		if options["now"]:
			return view_teacher_now(target)
		else:
			return view_teacher_weekday(target, options["weekday"])
	except:
		return JsonResponse({
			"message": {"text": "이름을 다시 한 번 확인하십시오."}})


@csrf_exempt
def answer(request):
	if now.weekday() >= 5:
		return JsonResponse({
			"message": {"text": "주말엔 좀 쉬자..(허걱)"}})
	try:
		input_request = request.body.decode("utf-8")
		input_json = json.loads(input_request)
		content = input_json["content"]

	except:
		return JsonResponse({
			"message": {"text": "Wrong input. 잘못된 접근입니다."}})
	else:
		if content == "도움말":
			with open(os.path.join(BASE_DIR, "response/etc/helper.txt")) as f:
				helper = f.read()
			return JsonResponse({
				"message": {"text": helper}})
		elif content == "지금":
			return JsonResponse({
				"message": {"text": now}})
		elif content == "오늘":
			return JsonResponse({
				"message": {"text": today + "요일"}})
		elif "검색" in content:
			return JsonResponse({
				"message": {"text": "키보드 작동중"}})

		else:
			# determine if an option exists
			try:
				contents = content.strip().split()
				assert len(contents) == 2 and contents[1] in  "지금 월 화 수 목 금".split()
				target = contents[0]
				if contents[1] == "지금":
					if len(target.split("-")) > 1:
						return view_class(target, {"now": True})
					else:
						# searching for teacher "now"
						return view_teacher(target, {"now": True})
				# searching for weekday
				else:
					if len(target.split("-")) > 1:
						return view_class(target, {"now": False, "weekday": contents[1]})
					else:
						# searching for teacher weekday
						return view_teacher(target, {"now": False, "weekday": contents[1]})

			# there's no option
			except:
				target = content.strip()
				if len(target.split("-")) > 1:
					return view_class(target, {"now": False, "weekday": today})
				else:
					return view_teacher(target, {"now": False, "weekday": today})









