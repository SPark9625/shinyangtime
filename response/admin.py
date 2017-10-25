from django.contrib import admin
from . import models

class TimeTableAdmin(admin.ModelAdmin):
	fields = ["year","semester","grade","division","subject","teacher","date","period"]
	fieldsets = [
		# (None, 				{"fields": ["default"]}),
		("Year/Semester", 	{"fields": ["year", "semester"]}),
		("Period related", 	{"fields": ["date", "period"]}),
		("Class related", 	{"fields": ["subject", "teacher", "grade", "division"]}),
	]

admin.site.register(models.TimeTable, TimeTableAdmin)