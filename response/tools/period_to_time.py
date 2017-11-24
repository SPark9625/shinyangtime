class Base:
	def start_end(instance):
		if instance.period == 1:
			return ["09:15", "10:00"]
		elif instance.period == 2:
			return ["10:10", "10:55"]
		elif instance.period == 3:
			return ["11:05", "11:50"]
		elif instance.period == 4:
			return ["12:00", "12:45"]
		elif instance.period == 5:
			return ["13:30", "14:15"]
		elif instance.period == 6:
			return ["14:25", "15:10"]
		elif instance.period == 7:
			return ["15:20", "16:05"]

class Custom:
	def start_end_2017_10_27(instance):
		if instance.period == 1:
			return ["09:10", "09:40"]
		elif instance.period == 2:
			return ["09:50", "10:20"]
		elif instance.period == 3:
			return ["10:30", "11:00"]
		elif instance.period == 4:
			return ["11:10", "11:40"]
		elif instance.period == 5:
			return ["11:50", "12:20"]
		elif instance.period == 6:
			return ["13:25", "13:55"]
		elif instance.period == 7:
			return ["00:00", "00:00"]

	def start_end_2017_10_31(instance):
		if instance.period == 1:
			return ["09:15", "09:55"]
		elif instance.period == 2:
			return ["10:05", "10:45"]
		elif instance.period == 3:
			return ["10:55", "11:35"]
		elif instance.period == 4:
			return ["11:45", "12:25"]
		elif instance.period == 5:
			return ["13:10", "13:45"]
		elif instance.period == 6:
			return ["13:55", "14:30"]
		elif instance.period == 7:
			return ["14:40", "15:15"]

	def start_end_2017_11_15(instance):
		if instance.period == 1:
			return ["09:15", "09:50"]
		elif instance.period == 2:
			return ["10:00", "10:35"]
		elif instance.period == 3:
			return ["10:45", "11:20"]
		elif instance.period == 4:
			return ["11:30", "12:05"]
		elif instance.period == 5:
			return ["12:15", "12:50"]
		elif instance.period == 6:
			return ["13:35", "14:20"]
		elif instance.period == 7:
			return ["14:30", "15:15"]

	def start_end_2017_11_22(instance):
		if instance.period == 1:
			return ["09:15", "09:50"]
		elif instance.period == 2:
			return ["10:00", "10:35"]
		elif instance.period == 3:
			return ["10:45", "11:20"]
		elif instance.period == 4:
			return ["11:30", "12:05"]
		elif instance.period == 5:
			return ["12:15", "12:50"]
		elif instance.period == 6:
			return ["13:35", "14:20"]
		elif instance.period == 7:
			return ["14:30", "15:15"]