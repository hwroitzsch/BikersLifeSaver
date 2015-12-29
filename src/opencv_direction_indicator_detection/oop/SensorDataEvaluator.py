__author__ = 'Hans-Werner Roitzsch'

from LEDController import LEDController
from SpeakerController import SpeakerController
from WarningLevel import WarningLevel
from RESTCommunicator import RESTCommunicator
from datetime import datetime

class SensorDataEvaluator:
	def __init__(self):
		self.led_controller = LEDController()
		self.speaker_controller = SpeakerController()
		self.rest_communicator = RESTCommunicator()

		self.minimum_time_elapsed_between_requests = 30  # 30s should pass before sending another request
		self.last_inform_server_datetime = None

	def evaluate(self, processed_sensor_data):
		print('evaluating sensor data')

		# TODO:
		# depending on where the data comes from,
		# what time it it,
		# and how reliable the data is,
		# a warning should be given and an event sent.

		if processed_sensor_data.result:  # if there is a warning according to the ProcessedSensorData object
			self.led_controller.start_warning(WarningLevel.DANGEROUS_SITUATION_WARNING.value)
			self.speaker_controller.start_warning(WarningLevel.DANGEROUS_SITUATION_WARNING.value)
			self.inform_server()
		else:
			self.led_controller.stop_warning()
			self.speaker_controller.stop_warning()

	# TODO: use asyncio???
	def inform_server(self):
		if self.last_inform_server_datetime is None:
			datetime_diff = self.minimum_time_elapsed_between_requests + 1  # greater than minimum in any case
		else:
			datetime_diff = datetime.now() - self.last_inform_server_datetime

		if datetime_diff.seconds >= 30:
			example_longitude = '58.33444'
			example_latitude = '19.72878'

			# create dictionary
			current_timestamp = time()
			current_datetime = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%S')
			print('sending request with timestamp:', current_datetime)

			self.rest_communicator.send_dangerous_traffic_situation_request(
				example_longitude,
				example_latitude,
				current_datetime
			)

			self.last_inform_server_datetime = current_datetime
		else:
			print('WARNING:', 'not informing server, because last request is less than', self.minimum_time_elapsed_between_requests, 'ago.')
