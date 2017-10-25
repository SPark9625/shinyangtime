from ..models import TimeTable
import datetime
def weekday(date=None):
	if date == None:
		date = datetime.datetime.now()
	return "월 화 수 목 금".split()[date.weekday()]

def late_night_message():
	with open(os.path.join(BASE_DIR, "response/etc/late_night_message.txt")) as f:
		ls = f.readlines()
	return [line.strip() for line in ls]

def validate_teacher(teacher):
	if teacher in TimeTable.TEACHER_LIST:
		return True
	else:
		return False