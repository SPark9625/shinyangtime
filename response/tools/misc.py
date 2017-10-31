from ..models import TimeTable
import datetime
def weekday(date=None):
	if date == None:
		date = datetime.datetime.now()
	return "월 화 수 목 금 토 일".split()[date.weekday()]

def weekday_rev(weekday):
	if weekday == "월":
		return 0
	if weekday == "화":
		return 1
	if weekday == "수":
		return 2
	if weekday == "목":
		return 3
	if weekday == "금":
		return 4

def late_night_message():
	with open(os.path.join(BASE_DIR, "response/etc/late_night_message.txt")) as f:
		ls = f.readlines()
	return [line.strip() for line in ls]

def validate_teacher(teacher):
	if teacher in TimeTable.TEACHER_LIST:
		return True
	else:
		return False

def period_time(inst):
	return "{}:{}~\n{}:{}".format(inst.start.hour, inst.start.minute, inst.end.hour, inst.end.minute)

def format_date(date):
	return "{}월 {}일".format(date.month, date.day)