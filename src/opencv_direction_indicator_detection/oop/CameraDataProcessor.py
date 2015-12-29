import time
import sched
import datetime
import cv2 as opencv
import numpy as np

from config import *

from SensorDataProcessor import SensorDataProcessor
from ProcessedCameraData import ProcessedCameraData
from ImageFileWriter import ImageFileWriter

__author__ = 'Hans-Werner Roitzsch'


class CameraDataProcessor(SensorDataProcessor):
	def __init__(self):
		self.image_file_writer = ImageFileWriter()
		self.processed_image_counter = 0

		print('using OpenCV version:', opencv.__version__)

		self.lower_blinker_hsv = np.uint8([80, 150, 220])
		self.upper_blinker_hsv = np.uint8([100, 220, 255])


	def create_kernel(self, rows=3, cols=3):
		return np.ones((rows, cols), dtype=np.int)

	def print_rows_cols(self, image):
		rows_and_cols = image.shape
		print('Rows and cols:', rows_and_cols)

	def add_border(self, image, top, bottom, left, right, color=0):
		return opencv.copyMakeBorder(
			image,
			top, bottom, left, right,
			opencv.BORDER_CONSTANT,
			value=color
		)

	def remove_border(self, image, top, bottom, left, right):
		rows_and_cols = image.shape
		return image[top:rows_and_cols[0] - bottom, left:rows_and_cols[1] - right]

	def process_data(self, camera_data):
		image = camera_data.data
		if image.shape is not None:
			# mean filter to reduce noise
			kernel = np.ones((6, 6), dtype=np.float32) / 36
			mean_filtered = opencv.filter2D(image, -1, kernel)

			# convert to HSV image
			hsv_image = opencv.cvtColor(mean_filtered, opencv.COLOR_RGB2HSV)

			# HSV color segmentation
			mask_image = opencv.inRange(hsv_image, self.lower_blinker_hsv, self.upper_blinker_hsv)  # select only the pixels with HSV in the given range

			# closing to make segments compact
			kernel = self.create_kernel(rows=40, cols=40)
			closing_image = opencv.morphologyEx(mask_image, opencv.MORPH_CLOSE, kernel)

			# create border around the image to create "fair" conditions for each pixel in the closing and erode step
			border_top = 3
			border_bottom = 3
			border_left = 3
			border_right = 3
			bordered_image = self.add_border(closing_image, border_top, border_bottom, border_left, border_right)

			# erode to remove noise
			kernel = self.create_kernel(rows=3, cols=3)
			eroded_image = opencv.erode(bordered_image, kernel=kernel, iterations=3)

			# remove border for bitwise AND operation with original image
			eroded_image = self.remove_border(
				eroded_image,
				border_top,
				border_bottom,
				border_left,
				border_right
			)

			# set the result
			result_image = eroded_image

			if any(255 in x for x in result_image):
				print('found direction indicator')

				# TODO: candidate for asyncIO???
				if config_development_mode:
					self.image_file_writer.write_images(
						'test_image_' + str(self.processed_image_counter) + '.PNG',
						image,
						'test_image_eroded_' + str(self.processed_image_counter) + '.PNG',
						result_image
					)
				return ProcessedCameraData(probability=100.0, result=True)
			else:
				print('no direction indicator found')
				return ProcessedCameraData(probability=100.0, result=False)

			self.processed_image_counter += 1
