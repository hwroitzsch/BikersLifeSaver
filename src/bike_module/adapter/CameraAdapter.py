import time
import picamera
import picamera.array
import numpy as np

from model.CameraData import CameraData
from adapter.SensorAdapter import SensorAdapter
from config import capture_format

__author__ = 'Hans-Werner Roitzsch'


class CameraAdapter(SensorAdapter):
	def __init__(self):
		try:
			self.camera = picamera.PiCamera()
			self.camera.resolution = (800, 600)
			self.camera.framerate = 24
			time.sleep(2)
		except Exception as ex:
			print('Problem with camera.')

	def get_data(self):
		with picamera.array.PiRGBArray(self.camera) as stream:
			self.camera.start_preview()
			self.camera.capture(stream, format=capture_format, use_video_port=True)
			timestamp = int(round(time.time() * 1000))

			parts = np.split(stream.array, 6)
			# use only the 3 vertical 1/6 of the picture, which are the 3rd, 4th and 5th parts
			image = np.concatenate((parts[2], parts[3], parts[4]), axis=0)

			return CameraData(image, timestamp)
