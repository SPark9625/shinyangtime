from ..models import TimeTable
from .misc import weekday

class Modifier:
	def change(grade, division, cell1, cell2):
		"""cells are dictionaries containing the following keys: date, period"""
		year = 2017
		semester = 2
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

	