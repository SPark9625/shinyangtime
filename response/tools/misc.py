from ..models import TimeTable
import datetime
import os
from timetable.settings import BASE_DIR

def weekday(date=None):
	if date == None:
		date = datetime.datetime.now()
	return "월 화 수 목 금 토 일".split()[date.weekday()]

def weekday_rev(weekday):
	if "월" in weekday:
		return 0
	if "화" in weekday:
		return 1
	if "수" in weekday:
		return 2
	if "목" in weekday:
		return 3
	if "금" in weekday:
		return 4

def late_night_message(now):
	with open(os.path.join(BASE_DIR, "response/etc/late_night_message.txt"), encoding='utf-8') as f:
		ls = f.readlines()
	if now.time() < datetime.time(6,00):
		ls.append("집에서 주무시고 계신데 왜요?(꺄아)")
	return ls

def validate_teacher(teacher):
	if teacher not in TimeTable.TEACHER_LIST:
		raise SyntaxError

def period_time(inst):
	sh = str(inst.start.hour).zfill(2)
	sm = str(inst.start.minute).zfill(2)
	eh = str(inst.end.hour).zfill(2)
	em = str(inst.end.minute).zfill(2)
	return "{}:{}~{}:{}".format(sh, sm, eh, em)

def format_date(now):
	return "{}월 {}일".format(now.month, now.day)


def no_class_now():
	return "지금은 수업중이 아닙니다.\n<최근 수업>"

def error(code, teacher=None, now=None, period=None):
	if code == 404:
		text = "Wrong path. 잘못된 접근입니다."
	elif code == "wrong_input":
		text = "입력 형식이 올바르지 않습니다.\n검색 방법을 보시려면 '도움말'을 입력해주세요."
	elif code == "no_class_today":
		text = "{}\n오늘은 수업이 없습니다.".format(format_date(now))
	elif code == "no_class_now":
		text = "지금은 수업중이 아닙니다.\n<최근 수업>"
	elif code == "no_class_today_teacher":
		text = "{}\n{} 선생님은 오늘 수업이 없습니다.".format(format_date(now), teacher)
	elif code == "weekend":
		text = "주말에는 지원하지 않는 서비스입니다."
	elif code == "not_yet":
		text = "{}\n오늘 {}선생님의 첫 수업은 {}교시부터입니다.".format(format_date(now), teacher, period)

	return text

def message_title(type, grade=None, division=None, teacher=None, date=None):
	pass

def class_period(period, subject, teacher):
	return "{}교시 {} {}".format(period, subject, teacher)

def weekday_tuner(now, option):
	if option == "오늘":
		wd = now.weekday()
	elif option == "어제":
		wd = (now - datetime.timedelta(days=1)).weekday()
	elif option == "내일":
		wd = (now + datetime.timedelta(days=1)).weekday()
	else:
		wd = weekday_rev(option)
		if now.weekday() > 4:
			now += datetime.timedelta(days=2)
	return now + datetime.timedelta(days=wd - now.weekday())