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
	def start_end_2017_Fall_13(instance):
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
