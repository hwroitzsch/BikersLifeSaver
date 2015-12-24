import time
import picamera
import picamera.array

from CameraData import CameraData
from SensorAdapter import SensorAdapter

__author__ = 'Hans-Werner Roitzsch'


class CameraAdapter(SensorAdapter):
	def __init__(self):
		pass

	def get_data(self):
		with picamera.PiCamera() as camera:
			camera.resolution = (1024, 768)
			camera.framerate = 24
			time.sleep(2)

			with picamera.array.PiRGBArray(camera) as stream:
				camera.start_preview()
				camera.capture(stream, format='rgb')

				timestamp = int(round(time.time() * 1000))
				return CameraData(stream.array, timestamp)
