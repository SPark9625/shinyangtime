# 해야 할 일:
# 1. 선생님과 교실도 옵션으로
# 2. 교실에 층 정보 추가
# 3. 교시를 선택하면 시작시간과 종료시간이 자동으로 디폴트 값이 나오도록 수정
# 4. 토,일요일 제거



from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

import json
import datetime
import random

from .models import TimeTable
import os

from timetable.settings import BASE_DIR



def keyboard(request):
	return JsonResponse({
		"type": "buttons",
		"buttons": ["도움말", "바로검색"]
	})

def late_night_message():
	return ["왜 이 시간에 이걸..(허걱)", "1교시 아직인데..(훌쩍)", "쉬고싶다..(부르르)", "이 사람아 지금 이걸 왜 해!(박력)", "1교시는 아침 9시부터입니다..(졸려)", "...(깜짝)", "..(짜증)", "나 잠 못자서 이러케돼써요..(헉)"]

def validate_teacher(teacher):
	if teacher in TimeTable.TEACHER_LIST:
		return True
	else:
		return False

now = datetime.datetime.now()

def weekday(date=None):
	if date == None:
		date = now
	return "월 화 수 목 금".split()[date.weekday()]

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
	periods = 7

	rows = TimeTable.objects.filter(grade=grade, division=division, weekday=weekday).order_by("period")
	l = list()
	for i in range(periods):
		try:
			l.append("{}교시 {}".format(i+1, rows[i].subject))
		except:
			l.append("{}교시 -".format(i+1))
	name = "{}학년 {}반({}요일):".format(grade, division, weekday)
	return JsonResponse({
		"message": {
			"text": "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(name, l[0], l[1], l[2], l[3], l[4], l[5], l[6])
		}
		})


# 선생님(오늘):
# 1교시 1-1
# 2교시 -
# 3교시 -
# 4교시 2-2
# 5교시 2-3
# 6교시 -
# 7교시 -
def view_teacher_weekday(teacher, weekday):
	if validate_teacher(teacher):
		periods = 7
		rows = list()
		for i in range(periods):
			try:
				row = TimeTable.objects.get(teacher=teacher, period=(i+1), weekday=weekday)
				rows.append("{}교시 {} {}-{}".format(i+1, row.subject, row.grade, row.division))
			except:
				rows.append("{}교시 -".format(i+1))
		name = "{}({}요일):".format(teacher, weekday)
		return JsonResponse(
				{
				"message": {
					"text": "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}".format(name, rows[0], rows[1], rows[2], rows[3], rows[4], rows[5], rows[6])
				}
				})
	else:
		raise SyntaxError


# 1학년 1반(4교시):
# 국어
# 선생님
# 교실
def view_class_now(grade, division):
	if now.time() < datetime.time(9,00):
		message = late_night_message()
		if now.time() < datetime.time(6,00):
			message.append("집에서 주무시고 계신데 왜요?(꺄아)")
		return JsonResponse(
			{
			"message": {
				"text": message[random.randint(0, len(message)-1)]
			}
			})

	row = TimeTable.objects.filter(grade=grade, division=division, weekday=today, start__lt=now).order_by("-period")[0]
	period = row.period
	name = "{}학년 {}반({}교시):".format(grade, division, period)
	teacher = row.teacher
	subject = row.subject

	if now.time() > row.end:
		message = "지금은 수업중이 아닙니다.\n<최근 수업>"
		name = "{}\n{}".format(message, name)
	return JsonResponse(
			{
			"message": {
				"text": "{}\n{}\n{}".format(name,subject,teacher)
			}
			})


# 선생님(4교시):
# 교실
# 1학년 1반
def view_teacher_now(teacher):
	if validate_teacher(teacher):
		if now.time() < datetime.time(9,00):
			message = late_night_message()
			if now.time() < datetime.time(6,00):
				message.append("집에서 주무시고 계신데 왜요?(꺄아)")
			return JsonResponse(
				{
				"message": {
					"text": message[random.randint(0, len(message)-1)]
				}
				})

		row = TimeTable.objects.filter(teacher=teacher, weekday=today, start__lt=now).order_by("-period")[0]
		period = row.period
		teacher = row.teacher
		name = "{}({}교시):".format(teacher, period)
		teachingDivision = "{}학년 {}반".format(row.grade, row.division)
		subject = row.subject

		if now.time() > row.end:
			message = "지금은 수업중이 아닙니다.\n<최근 수업>"
			name = "{}\n{}".format(message, name)
		return JsonResponse(
				{
				"message": {
					"text": "{}\n{}".format(name,teachingDivision)
				}
				})
	else:
		raise SyntaxError


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
			with open(os.path.join(BASE_DIR, "response/helper.txt")) as f:
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









