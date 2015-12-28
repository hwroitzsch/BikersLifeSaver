from abc import ABCMeta, abstractmethod, abstractproperty

__author__ = 'Hans-Werner Roitzsch'


class SensorAdapter(metaclass=ABCMeta):
	"""
	Abstract Base Class: SensorAdapter
	"""

	@abstractmethod
	def get_data(self):
		return
