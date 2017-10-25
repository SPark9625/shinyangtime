# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

def start(s):
	if s.period == 1:
		return "09:15"
	elif s.period == 2:
		return "10:10"
	elif s.period == 3:
		return "11:05"
	elif s.period == 4:
		return "12:00"
	elif s.period == 5:
		return "13:30"
	elif s.period == 6:
		return "14:25"
	elif s.period == 7:
		return "15:20"

def end(s):
	if s.period == 1:
		return "10:00"
	elif s.period == 2:
		return "10:55"
	elif s.period == 3:
		return "11:50"
	elif s.period == 4:
		return "12:45"
	elif s.period == 5:
		return "14:15"
	elif s.period == 6:
		return "15:10"
	elif s.period == 7:
		return "16:05"


class TimeTable(models.Model):
	SEMESTER_CHOICES = zip([1,2],[1,2])

	WEEKDAY_LIST = ["월", "화", "수", "목", "금"]
	WEEKDAY_CHOICES = zip(WEEKDAY_LIST, WEEKDAY_LIST)
	SUBJECT_LIST = sorted(["국어","수학","영어","사회","과학","역사","도덕","철학","체육","기술가정","주제","미술","창체","동아", "음악", "진로", "예체", "스포츠", "한문"])
	SUBJECT_CHOICES = zip(SUBJECT_LIST, SUBJECT_LIST)
	PERIOD_CHOICES = zip([1,2,3,4,5,6,7],[1,2,3,4,5,6,7])
	GRADE_CHOICES = zip([1,2,3],[1,2,3])
	DIVISION_CHOICES = zip([1,2,3],[1,2,3])

	TEACHER_LIST = sorted(["장현선","김한나","현미숙","이경희","장윤일","정성진","김미경","최춘호","임성오","강학주","오인애","배근아","조은숙","유세정","김준영","도레미","김홍진","김지인","송유경","조은희","조진향","이득효"])
	TEACHER_CHOICES = zip(TEACHER_LIST, TEACHER_LIST)

	LOCATION_LIST = ["---1층---", "시청각실", "농구장", "운동장", "---2층---", "기술가정실", "컴퓨터실", "과학실1", "강당", "우정반", "---3층---", "3-1", "3-2", "3-3", "도서실", "인사랑1", "인사랑2", "인사랑3", "---4층---", "2-1", "2-2", "2-3", "동아리실1", "동아리실2", "Wee 클래스", "과학실2", "English Studio", "---5층---", "1-1", "1-2", "미술실", "음악실", "수사랑1", "수사랑2", "역사랑", "진로상담실", "--알수없음--"]
	CLASSROOM_CHOICES = zip(LOCATION_LIST, LOCATION_LIST)

	default = models.BooleanField(verbose_name="기본값", default=True)
	year = models.PositiveSmallIntegerField(verbose_name="년도", default=2017)
	semester = models.PositiveSmallIntegerField(verbose_name="학기", choices=SEMESTER_CHOICES, default=2)
	date = models.DateField(null=True, blank=True)
	weekday = models.CharField(max_length=30,choices=WEEKDAY_CHOICES, verbose_name="요일", default="월")
	period = models.PositiveSmallIntegerField(choices=PERIOD_CHOICES, verbose_name="교시", default=1)
	subject = models.CharField(max_length=30, choices=SUBJECT_CHOICES, verbose_name="과목")
	teacher = models.CharField(max_length=30, verbose_name="선생님", choices=TEACHER_CHOICES)
	grade = models.PositiveSmallIntegerField(choices=GRADE_CHOICES, verbose_name="학년", default=1)
	division = models.PositiveSmallIntegerField(choices=DIVISION_CHOICES, verbose_name="반", default=1)
	start = models.TimeField(verbose_name="시작시간", default="09:00")
	end = models.TimeField(verbose_name="종료시간", default="09:01")


	def __str__(self):
		return "{}요일 {}학년 {}반 {}교시 {}".format(self.weekday, self.grade, self.division, self.period, self.subject)






@receiver(pre_save, sender=TimeTable)
def my_handler(sender, instance, **kwargs):
	if instance.date:
		instance.weekday = TimeTable.WEEKDAY_LIST[instance.date.weekday()]
	if instance.period:
		instance.start = start(instance)
		instance.end = end(instance)


