from abc import ABCMeta, abstractmethod, abstractproperty

from WarningLevel import WarningLevel

__author__ = 'Hans-Werner Roitzsch'

class ActorController(metaclass=ABCMeta):
	"""
	Abstract Base Class: ActorController
	"""

	@abstractmethod
	def start_warning(self, warning_level):
		"""This method warns a traffic participant about a dangerous traffic situation and HazardSpots."""
		return

	@abstractmethod
	def stop_warning(self)
