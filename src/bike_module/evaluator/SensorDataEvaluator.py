__author__ = 'Hans-Werner Roitzsch'

from controller.LEDController import LEDController
from controller.SpeakerController import SpeakerController
from model.WarningLevel import WarningLevel
from network.RESTCommunicator import RESTCommunicator
from adapter.GPSSensorAdapter import GPSSensorAdapter

from datetime import datetime
from time import time

import config

class SensorDataEvaluator:
	def __init__(self):
		self.led_controller = LEDController()
		self.speaker_controller = SpeakerController()
		self.rest_communicator = RESTCommunicator()
		self.gps_sensor_adapter = GPSSensorAdapter()

		self.minimum_time_elapsed_between_requests = 30  # 30s should pass before sending another request
		self.last_inform_server_datetime = None

	def evaluate(self, processed_sensor_data):
		if config.development_mode:
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
			datetime_diff = (datetime.now() - self.last_inform_server_datetime).seconds

		if datetime_diff >= 30:
			# example_longitude = '58.33444'
			# example_latitude = '19.72878'

			# create dictionary
			current_datetime = datetime.fromtimestamp(time()).strftime('%Y-%m-%dT%H:%M:%S')
			
			if config.development_mode:
				print('sending request with timestamp:', current_datetime)

			current_gps_sensor_data = self.gps_sensor_adapter.get_data()
			longitude = current_gps_sensor_data['longitude']
			latitude = current_gps_sensor_data['latitude']
			# gps_datetime = datetime.fromtimestamp(current_gps_sensor_data['time_utc']).strftime('%Y-%m-%dT%H:%M:%SZ')
			# print('sending request with timestamp:', timestamp)


			self.rest_communicator.send_dangerous_traffic_situation_request(longitude, latitude, current_datetime)

			self.last_inform_server_datetime = datetime.now()
		else:
			print('WARNING:', 'not informing server, because last request is less than', self.minimum_time_elapsed_between_requests, 'ago.')
