from model.ProcessedSensorData import ProcessedSensorData

__author__ = 'Hans-Werner Roitzsch'


class ProcessedCameraData(ProcessedSensorData):
	def __init__(self, probability=100.0, result=True):
		self.probability = probability
		self.result = result
