# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from response.tools.period_to_time import Base, Custom

import datetime
from django.utils import timezone



class TimeTable(models.Model):
	SEMESTER_CHOICES = zip([1,2],["봄","가을"])

	WEEKDAY_LIST = ["월", "화", "수", "목", "금"]
	WEEKDAY_CHOICES = zip(WEEKDAY_LIST, WEEKDAY_LIST)
	SUBJECT_LIST = sorted('국어 수학 사회 과학 기가 영어 창체 민주 음악 미술 체육 스포츠 진로 예체 도덕 한문 역사 동아'.split())
	SUBJECT_CHOICES = zip(SUBJECT_LIST, SUBJECT_LIST)
	PERIOD_CHOICES = zip([1,2,3,4,5,6,7],[1,2,3,4,5,6,7])
	GRADE_CHOICES = zip([1,2,3],[1,2,3])
	DIVISION_CHOICES = zip([1,2,3],[1,2,3])

	TEACHER_LIST = '장현선 김한나 장윤일 현미숙 김미경 정성진 전청 김세열 이주호 박희연 배근아 임성오 유세정 조명희 이선숙 이경희 권지은 최미정 이득효 강유경'.split()
	TEACHER_CHOICES = list(zip(TEACHER_LIST, range(1, 21)))

	LOCATION_LIST = ["---1층---", "시청각실", "농구장", "운동장", "---2층---", "기술가정실", "컴퓨터실", "과학실1", "강당", "우정반", "---3층---", "3-1", "3-2", "3-3", "도서실", "인사랑1", "인사랑2", "인사랑3", "---4층---", "2-1", "2-2", "2-3", "동아리실1", "동아리실2", "Wee 클래스", "과학실2", "English Studio", "---5층---", "1-1", "1-2", "미술실", "음악실", "수사랑1", "수사랑2", "역사랑", "진로상담실", "--알수없음--"]
	CLASSROOM_CHOICES = zip(LOCATION_LIST, LOCATION_LIST)

	default = models.BooleanField(verbose_name="기본값", default=True)
	modified = models.BooleanField(verbose_name="변경사항", default=False)

	# auto
	year = models.PositiveSmallIntegerField(verbose_name="년도", blank=True, null=True)
	semester = models.PositiveSmallIntegerField(verbose_name="학기", choices=SEMESTER_CHOICES, null=True, blank=True)
	weekday = models.CharField(max_length=30,choices=WEEKDAY_CHOICES, verbose_name="요일", blank=True)

	date = models.DateField()
	period = models.PositiveSmallIntegerField(choices=PERIOD_CHOICES, verbose_name="교시", default=1)
	subject = models.CharField(max_length=30, choices=SUBJECT_CHOICES, verbose_name="과목")
	teacher = models.CharField(max_length=30, verbose_name="선생님", choices=TEACHER_CHOICES)
	grade = models.PositiveSmallIntegerField(choices=GRADE_CHOICES, verbose_name="학년", default=3)
	division = models.PositiveSmallIntegerField(choices=DIVISION_CHOICES, verbose_name="반", default=2)

	# auto
	start = models.TimeField(verbose_name="시작시간", null=True, blank=True)
	end = models.TimeField(verbose_name="종료시간", null=True, blank=True)


	def __str__(self):
		return "{} {} {}학년 {}반 {}교시 {}".format(self.date.strftime("%Y-%m-%d"), self.weekday, self.grade, self.division, self.period, self.subject)

@receiver(pre_save, sender=TimeTable)
def my_handler(sender, instance, **kwargs):
	if instance.date:
		instance.weekday = TimeTable.WEEKDAY_LIST[instance.date.weekday()]
		instance.year = instance.date.year
		if instance.date.month < 8:
			instance.semester = 1
		else:
			instance.semester = 2
	if not (instance.start and instance.end):
		Base.base(instance)


class Query(models.Model):
	teacher = models.CharField(blank=True, max_length=30)
	grade_division = models.CharField(blank=True, max_length=20)
	option = models.CharField(blank=True, max_length=10)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "{} {} {}, 날짜시간: {}".format(str(self.teacher), str(self.grade_division), str(self.option), self.date.strftime("%Y년 %m월 %d일 %H:%M"))

