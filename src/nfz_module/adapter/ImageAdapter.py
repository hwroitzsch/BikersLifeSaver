__author__ = 'Hans-Werner Roitzsch'

import time
import picamera
import picamera.array
import numpy as np

from model.CameraData import CameraData
from adapter.SensorAdapter import SensorAdapter
from config import capture_format
from reader.ImageReader import ImageReader

import config


class ImageAdapter(SensorAdapter):
	def __init__(self):
		self.image_reader = ImageReader()

	def get_data(self):
		timestamp = int(round(time.time() * 1000))
		image = self.image_reader.read_next()
		
		if config.development_mode:
			print('IMAGE TYPE in ImageAdapter:', type(image))

		return CameraData(self.image_reader.read_next(), timestamp)