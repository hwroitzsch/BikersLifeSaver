__author__ = 'Hans-Werner Roitzsch'
__date__ = '2015-12-29'


class GPSSensorAdapter(SensorAdapter):
	
	def __init__(self):
		self.last_values = {}
		self.gpsc = GPSController()
		try:
			self.gpsc.start()
		except:
			print('ERROR:', 'Could not start GPSController.')


	def get_data_from_controller(self):
		self.last_values['latitude'] = self.gpsc.fix.latitude
		self.last_values['longitude'] = self.gpsc.fix.longitude

		self.last_values['time_utc'] = self.gpsc.utc
		self.last_values['time'] = self.gpsc.fix.time

		self.last_values['altitude'] = self.gpsc.fix.altitude

		self.last_values['eps'] = self.gpsc.fix.eps
		self.last_values['epx'] = self.gpsc.fix.epx
		self.last_values['epv'] = self.gpsc.fix.epv
		self.last_values['ept'] = self.gpsc.gpsd.fix.ept

		self.last_values['speed'], self.gpsc.fix.speed

		self.last_values['climb'], self.gpsc.fix.climb

		self.last_values['track'], self.gpsc.fix.track

		self.last_values['mode'], self.gpsc.fix.mode

		self.last_values['sats'], self.gpsc.satellites

		return self.last_values
