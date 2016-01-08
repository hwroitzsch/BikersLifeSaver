import time
import picamera
import picamera.array

from CameraData import CameraData
from SensorAdapter import SensorAdapter

__author__ = 'Hans-Werner Roitzsch'


class CameraAdapter(SensorAdapter):
	def __init__(self):
		try:
			self.camera = picamera.PiCamera()
			self.camera.resolution = (1024, 768)
			self.camera.framerate = 24
			time.sleep(2)
		except Exception as ex:
			print('Problem with camera.')

	def get_data(self):
		# with picamera.PiCamera() as camera:
		# 	camera.resolution = (1024, 768)
		# 	camera.framerate = 24
		# 	time.sleep(2)

			# with picamera.array.PiRGBArray(camera) as stream:
			# 	camera.start_preview()
			# 	camera.capture(stream, format='rgb')
			#
			# 	timestamp = int(round(time.time() * 1000))
			# 	return CameraData(stream.array, timestamp)

		with picamera.array.PiRGBArray(self.camera) as stream:
			self.camera.start_preview()
			# self.camera.capture(stream, format='rgb')
			# self.camera.capture(stream, format='bgr')
			self.camera.capture(stream, format='bgr', use_video_port=True)

			timestamp = int(round(time.time() * 1000))
			return CameraData(stream.array, timestamp)
