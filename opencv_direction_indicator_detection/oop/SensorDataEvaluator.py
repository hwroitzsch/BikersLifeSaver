__author__ = 'Hans-Werner Roitzsch'

class SensorDataEvaluator:
	def __init__(self):
		pass

	def evaluate(processed_sensor_data):
		# TODO:
		# depending on where the data comes from,
		# what time it it,
		# and how reliable the data is,
		# a warning should be given and an event sent.

		if processed_sensor_data.result:
			self.led_controller.start_warning(WarningLevel.DANGEROUS_SITUATION_WARNING)
			self.speaker_controller.start_warning(WarningLevel.DANGEROUS_SITUATION_WARNING)
			# TODO: Send a message to the server about the dangerous situation event
