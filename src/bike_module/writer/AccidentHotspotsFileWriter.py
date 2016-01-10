__author__ = 'Hans-Werner Roitzsch'
__date__ = '2015-12-29'

class AccidentHotspotsFileWriter:
	"""docstring for AccidentHotspotsFileWriter"""
	def __init__(self):
		pass


	# TODO: maybe we should use asyncio here???
	@classmethod
	def write_accident_hotspots_to_file(
		self,
		accident_hotspots_data, file_path='/root/ghisallo_venv/src/opencv_direction_indicator_detection/oop/data/accident_hotspots.json'
	):
		"""This method writes accident hotspots to a file."""
		try:
			with open(file_path, 'w') as accident_hotspots_file:
				json.dump(accident_hotspots_data, accident_hotspots_file)
		except Exception as ex:
			print('ERROR: Could not write accident hotspots to file.')
