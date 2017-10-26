from ..models import TimeTable
from .misc import weekday
from .period_to_time import Custom

year = 2017
semester = 2

class Modifier:
	def base_copy(grade, division, date, period):
		t = TimeTable.objects.get(default=True, grade=grade, division=division, weekday=weekday, period=period)
		new = TimeTable.objects.create(
			default = False,
			year = year,
			semester = semester,
			date = date,
			period = period,
			subject = t.subject,
			teacher = t.teacher,
			grade = grade,
			division = division
		)
		print(new)

	def change(grade, division, cell1, cell2):
		"""cells are dictionaries containing the following keys: date, period"""
		# dates
		wd1 = weekday(cell1["date"])
		wd2 = weekday(cell2["date"])
		# periods
		c1 = TimeTable.objects.get(default=True, grade=grade, division=division, weekday=wd1, period=cell1["period"])
		c2 = TimeTable.objects.get(default=True, grade=grade, division=division, weekday=wd2, period=cell2["period"])
		s1 = c1.subject
		s2 = c2.subject
		t1 = c1.teacher
		t2 = c2.teacher
		# grade
		# division

		new1 = TimeTable.objects.create(
			default = False,
			year = year,
			semester = semester,
			date = cell2["date"],
			period = cell2["period"],
			subject = s1,
			teacher = t1,
			grade = grade,
			division = division
		)
		new2 = TimeTable.objects.create(
			default = False,
			year = year,
			semester = semester,
			date = cell1["date"],
			period = cell1["period"],
			subject = s2,
			teacher = t2,
			grade = grade,
			division = division
		)
		print(new1)
		print(new2)

	def date_time_mod(grade, division, date, func):
		# 1. 이미 존재하는 셀들 전부 가져옴.
		# 2. 1번의 셀들 제외하고 전부 베이스에서 복붙
		# 3. 그 날짜 전체 시간 조정.
		wd = weekday(date)
		existing_rows = TimeTable.objects.filter(default=False, date=date, grade=grade, division=division)
		existing_periods = list()
		base_rows = len(TimeTable.objects.filter(default=True, weekday=wd, grade=grade, division=division))
		for row in existing_rows:
			existing_periods.append(row.period)
		for i in range(base_rows):
			if i+1 not in existing_periods:
				base_copy(grade, division, date, i+1)
		targets = TimeTable.objects.filter(default=False, date=date, grade=grade, division=division)
		for target in targets:
			target.start, target.end = Custom.start_end_2017_10_27(target)
			print(target, target.start, target.end)