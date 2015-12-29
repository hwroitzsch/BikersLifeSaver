import requests
import json
from time import time
from datetime import datetime

from NetworkCommunicator import NetworkCommunicator
from AccidentHotspotsFileWriter import AccidentHotspotsFileWriter

__author__ = 'Konstantin Bychkov, Hans-Werner Roitzsch'
__date__ = "2015-12-29"

class RESTCommunicator(NetworkCommunicator):
	def __init__(self):
		self.server_communication_protocol = 'http'
		self.server_ip_address = '85.214.69.226'
		self.server_port = 8080

	# def print_get_accident_hotspot_response_information(self, response):
	# 	"""This method prints information in the terminal."""
	#
	# 	# check if the request has been handled successully
	# 	if response.status_code == requests.codes.ok:
	# 		print('RESPONSE:OK')
	# 	else:
	# 		print('WARNING: Request was not handled successfully.')
	#
	# 	# print information about the response header
	# 	print('Content-Type:')
	# 	print(response.headers.get('content-type'))
	# 	print(response.headers)
	#
	# 	# print received response
	# 	print('received RESPONSE:')
	# 	print(response.text)

	# def get_accident_hotspots(self):
	# 	"""This method sends a request to the server, in order to receive a set of accident spots as a response."""
	#
	# 	# define the header
	# 	# we expect the server to respond with a JSON object
	# 	headers = {'Accept': 'application/json'}
	#
	# 	# send the request to the server
	# 	response = requests.get(
	# 		'http://85.214.69.226:8080/WebServiceBLS/webresources/accidentspots',
	# 		headers=headers
	# 	)
	#
	# 	# print some information about the response
	# 	self.print_get_accident_hotspot_response_information(response)
	#
	# 	# write the received accident hotspot data to a file
	# 	accident_hotspots_data = response.json()
	#
	# 	AccidentHotspotsFileWriter.write_accident_hotspots_to_file(accident_hotspots_data)


	# TODO: this might be a good candidate for a method using asyncio
	def print_send_dangerous_situation_response_information(self, response, coordinates):
		"""This method prints information about the received response for a request, which informs the server about a detected dangerous traffic situation."""

		print('created JSON:')
		print(json.dumps(coordinates))

		# check whether the request was handled successfully
		if response.status_code == requests.codes.ok:
			print('RESPONSE:OK')
		else:
			print('WARNING: request not handled successfully')

		print('The status code is:', response.status_code)

		if response.status_code == 204:
			print('(Position has been saved. The response is without a message-body.)')
		elif response.status_code == 201:
			print('(Position has been saved. The request has been fulfilled.)')

	# TODO: use asyncio ???
	def send_dangerous_traffic_situation_request(self, latitude, longitude, current_datetime):
		"""This method sends the current coordinates and a timestamp to the server. With this information the server can calculate accident hotspots."""

		current_coordinates = {
			'longitude': longitude,
			'latitude': latitude,
			'timeStamp': current_datetime
		}

		# define header, we will send a JSON object to the server
		headers = {'content-type': 'application/json'}

		# url = 'http://85.214.69.226:8080/WebServiceBLS/webresources/receivedcoordinates'
		url = self.server_communication_protocol + '://' + self.server_ip_address + ':' + str(self.server_port) + '/WebServiceBLS/webresources/receivedcoordinates'

		# send request to the server to persist the current geo location
		# hold the response in a variable
		response = requests.post(url, data=json.dumps(current_coordinates), headers=headers)

		# print information about the received response
		self.print_send_dangerous_situation_response_information(response, coordinates)
