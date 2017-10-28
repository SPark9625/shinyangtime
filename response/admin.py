from django.contrib import admin
from response import models

class TimeTableAdmin(admin.ModelAdmin):
	list_filter = ["default","modified","year","semester","date","grade","division"]
	# fieldsets = [
	# 	# (None, 				{"fields": ["default"]}),
	# 	# ("Year/Semester", 	{"fields": ["year", "semester"]}),
	# 	("Period related", 	{"fields": ["date", "period"]}),
	# 	("Class related", 	{"fields": ["subject", "teacher", "grade", "division"]}),
	# ]

admin.site.register(models.TimeTable, TimeTableAdmin)