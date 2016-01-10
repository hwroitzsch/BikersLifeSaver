
class TimeFunction:
	def __init__(self):
		pass

	@classmethod
	def calculate_time_diff(self, t1, t2):
		return (t2 - t1).microseconds / (1 * 10**6) + (t2 - t1).seconds