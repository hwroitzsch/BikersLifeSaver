__author__ = 'Hans-Werner Roitzsch'

class CameraData(SensorData):
	def __init__(self, data, timestamp):
		self.data = data
		self.timestamp = timestamp
