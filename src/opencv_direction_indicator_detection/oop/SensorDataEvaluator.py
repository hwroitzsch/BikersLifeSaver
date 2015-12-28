__author__ = 'Hans-Werner Roitzsch'

from LEDController import LEDController
from SpeakerController import SpeakerController
from WarningLevel import WarningLevel

class SensorDataEvaluator:
	def __init__(self):
		self.led_controller = LEDController()
		self.speaker_controller = SpeakerController()

	def evaluate(self, processed_sensor_data):
		# TODO:
		# depending on where the data comes from,
		# what time it it,
		# and how reliable the data is,
		# a warning should be given and an event sent.

		if processed_sensor_data.result:
			self.led_controller.start_warning(WarningLevel.DANGEROUS_SITUATION_WARNING.value)
			self.speaker_controller.start_warning(WarningLevel.DANGEROUS_SITUATION_WARNING.value)
			# TODO: Send a message to the server about the dangerous situation event
