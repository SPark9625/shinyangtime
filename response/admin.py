from django.contrib import admin
from . import models

class TimeTableAdmin(admin.ModelAdmin):
	fields = "__all__"
	fieldsets = [
		(None, 				{"fields": ["default"]}),
		("Year/Semester", 	{"fields": ["year", "semester"]}),
		("Period related", 	{"fields": ["date", "weekday", "period", "start", "end"]}),
		("Class related", 	{"fields": ["subject", "teacher", "grade", "division"]}),
	]

admin.site.register(models.TimeTable, TimeTableAdmin)