# -*- coding: utf-8 -*-

from ..models import TimeTable
from .misc import weekday
from .period_to_time import Base, Custom
from shinyang import SHINYANG, this_year, this_semester
import datetime

def refresh(query):
	"""refreshes to new state"""
	for row in query:
		row.year = row.date.year
		if row.date.month < 8:
			row.semester = 1
		else:
			row.semester = 2
		row.weekday = weekday(row.date)
		row.start, row.end = Base.start_end(row)
		row.save()
		print(row)



def base_cell_copy(grade, division, date, period):
	"""input: grade, division, date, period
	Creates a new cell at the given date and prints it.
	Doesn't return anything"""
	if isinstance(date, str):
		date = datetime.datetime.strptime(date, "%Y-%m-%d")
	try:
		t = TimeTable.objects.get(default=False, grade=grade, division=division, date=date, period=period)
		print(t, "overwrite not possible.")
	except:
		wd = weekday(date)
		t = TimeTable.objects.get(default=True, grade=grade, division=division, weekday=wd, period=period)
		new = TimeTable.objects.create(
			default = False,
			modified = False,
			year = this_year,
			semester = this_semester,
			date = date,
			period = period,
			subject = t.subject,
			teacher = t.teacher,
			grade = grade,
			division = division
		)
		print(new)

def base_day_copy(grade, division, date):
	"""input: grade, division, date"""
	if isinstance(date, str):
			date = datetime.datetime.strptime(date, "%Y-%m-%d")
	wd = weekday(date)
	periods = SHINYANG[this_year][this_semester]["PERIODS"][wd]
	for p in range(periods):
		base_cell_copy(grade, division, date, p+1)

def base_cell_copy_z(date, period):
	"""input: date, period"""
	if isinstance(date, str):
			date = datetime.datetime.strptime(date, "%Y-%m-%d")
	wd = weekday(date)
	for gd in SHINYANG[this_year][this_semester]["GRADE_DIVISION"]:
		base_cell_copy(gd[0], gd[1], date, period)

def base_day_copy_z(date):
	"""input: date
	For the given date, copies the base timetable for all grades and divisions"""
	if isinstance(date, str):
			date = datetime.datetime.strptime(date, "%Y-%m-%d")
	for gd in SHINYANG[this_year][this_semester]["GRADE_DIVISION"]:
		base_day_copy(gd[0], gd[1], date)



class Modifier:
	def interchange(grade, division, cell1, cell2):
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
			modified = True,
			year = this_year,
			semester = this_semester,
			date = cell2["date"],
			period = cell2["period"],
			subject = s1,
			teacher = t1,
			grade = grade,
			division = division
		)
		new2 = TimeTable.objects.create(
			default = False,
			modified = True,
			year = this_year,
			semester = this_semester,
			date = cell1["date"],
			period = cell1["period"],
			subject = s2,
			teacher = t2,
			grade = grade,
			division = division
		)
		print(new1)
		print(new2)

	def timerange_change(date, func):
		# 1. 이미 존재하는 셀들 전부 가져옴.
		# 2. 1번의 셀들 제외하고 전부 베이스에서 복붙
		# 3. 그 날짜 전체 시간 조정.
		if isinstance(date, str):
			date = datetime.datetime.strptime(date, "%Y-%m-%d")
		for gd in SHINYANG["2017"]["2"]["GRADE_DIVISION"]:
			grade = gd[0]
			division = gd[1]
			wd = weekday(date)
			existing_rows = TimeTable.objects.filter(default=False, date=date, grade=grade, division=division)
			existing_periods = list()
			base_periods = SHINYANG["2017"]["2"]["PERIODS"][wd]
			for row in existing_rows:
				existing_periods.append(row.period)
			for i in range(base_periods):
				if i+1 not in existing_periods:
					base_cell_copy(grade, division, date, i+1)

			targets = TimeTable.objects.filter(default=False, date=date, grade=grade, division=division)
			for target in targets:
				target.start, target.end = func(target)
				target.save()
				print(target, target.start, target.end)