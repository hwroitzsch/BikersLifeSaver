from datetime import datetime

__author__ = 'Hans-Werner Roitzsch'

class Event:
	def __init__(
		self,
		timestamp=datetime.now(),
		transmitter_id,
		transmitter_type_id,
		longitude,
		latitude
	):
		self.timestamp = timestamp
		self.transmitter_id = transmitter_id
		self.longitude = longitude
		self.latitude = latitude
		self.transmitter_type = transmitter_type
