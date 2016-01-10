from abc import ABCMeta, abstractmethod, abstractproperty

__author__ = 'Hans-Werner Roitzsch'


class SensorDataProcessor(metaclass=ABCMeta):
	"""
	Abstract Base Class: SensorDataProcessor
	"""

	@abstractmethod
	def process_data(self, sensor_data):
		return
