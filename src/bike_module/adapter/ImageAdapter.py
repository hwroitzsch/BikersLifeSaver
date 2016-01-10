import time
import picamera
import picamera.array
import numpy as np

from model.CameraData import CameraData
from adapter.SensorAdapter import SensorAdapter
from config import capture_format

__author__ = 'Hans-Werner Roitzsch'


class ImageAdapter(SensorAdapter):
	def __init__(self):
		self.image_reader = ImageReader()

	def get_data(self):
		timestamp = int(round(time.time() * 1000))
		return CameraData(self.image_reader.read_next(), timestamp)