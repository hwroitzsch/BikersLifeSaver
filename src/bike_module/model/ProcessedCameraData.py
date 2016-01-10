from model.ProcessedSensorData import ProcessedSensorData

__author__ = 'Hans-Werner Roitzsch'


class ProcessedCameraData(ProcessedSensorData):
	def __init__(self, probability, result):
		self.probability = probability
		self.result = result
