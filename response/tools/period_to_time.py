def save(instance, start_end_list):
	p = instance.period - 1
	instance.start, instance.end = start_end_list[p]
	instance.save()

def update(instances, fn):
	for instance in instances:
		fn(instance)

class Base:
	def base(instance):
		start_end_list = [
					("09:15", "10:00"),
					("10:10", "10:55"),
					("11:05", "11:50"),
					("12:00", "12:45"),
					# lunch 45m
					("13:30", "14:15"),
					("14:25", "15:10"),
					("15:20", "16:05"),
					]
		save(instance, start_end_list)

class Custom:
	def type1(instance):
		start_end_list = [
					("09:10", "09:40"),  # 30m
					("09:50", "10:20"),  # 30m
					("10:30", "11:00"),  # 30m
					("11:10", "11:40"),  # 30m
					("11:50", "12:20"),  # 30m
					# lunch 1h 5m
					("13:25", "13:55"),  # 30m
					("00:00", "00:00"),
					]
		save(instance, start_end_list)

	def type2(instance):
		start_end_list = [
					("09:15", "09:55"),  # 40m
					("10:05", "10:45"),  # 40m
					("10:55", "11:35"),  # 40m
					("11:45", "12:25"),  # 40m
					# lunch 45m
					("13:10", "13:45"),  # 35m
					("13:55", "14:30"),  # 35m
					("14:40", "15:15"),  # 35m
					]
		save(instance, start_end_list)

	def type3(instance):
		start_end_list = [
					("09:15", "09:50"),  # 35m
					("10:00", "10:35"),  # 35m
					("10:45", "11:20"),  # 35m
					("11:30", "12:05"),  # 35m
					("12:15", "12:50"),  # 35m
					# lunch 45m
					("13:35", "14:20"),  # 45m
					("14:30", "15:15"),  # 45m
					]
		save(instance, start_end_list)

	def type4(instance):
		start_end_list = [
					("09:15", "09:45"),  # 30m
					("09:55", "10:25"),  # 30m
					("10:35", "11:05"),  # 30m
					("11:15", "11:45"),  # 30m
					("11:55", "12:25"),  # 30m
					# lunch 45m
					("13:10", "13:40"),  # 30m
					("13:50", "14:20"),  # 30m
					]
		save(instance, start_end_list)

	def type5(instance):
		start_end_list = [
					("09:15", "09:55"),  # 40m
					("10:05", "10:45"),  # 40m
					("10:55", "11:35"),  # 40m
					("11:45", "12:25"),  # 40m
					# lunch 45m
					("13:10", "13:50"),  # 40m
					("14:00", "14:40"),  # 40m
					("14:50", "15:30"),  # 40m
					]
		save(instance, start_end_list)

	def type6(instance):
		start_end_list = [
					("09:15", "09:45"),  # 30m
					("09:55", "10:25"),  # 30m
					("10:35", "11:05"),  # 30m
					("11:15", "11:45"),  # 30m
					("11:55", "12:25"),  # 30m
					# lunch 45m
					("13:10", "13:40"),  # 30m
					("00:00", "00:00"),
					]
		save(instance, start_end_list)
