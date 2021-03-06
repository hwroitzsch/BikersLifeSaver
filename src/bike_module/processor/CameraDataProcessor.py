__author__ = 'Hans-Werner Roitzsch'


from datetime import datetime

import sched
import cv2 as opencv
import numpy as np

from config import *

from processor.SensorDataProcessor import SensorDataProcessor
from model.ProcessedCameraData import ProcessedCameraData
from writer.ImageFileWriter import ImageFileWriter


class CameraDataProcessor(SensorDataProcessor):
	def __init__(self):
		self.image_file_writer = ImageFileWriter()
		self.processed_image_counter = 0

		print('using OpenCV version:', opencv.__version__)

		# self.lower_blinker_hsv = np.uint8([80, 150, 220])
		# self.upper_blinker_hsv = np.uint8([100, 220, 255])

		self.lower_blinker_hsv = np.uint8([260, 150, 220])  # 360° - 80°
		self.upper_blinker_hsv = np.uint8([280, 220, 255])  # 360° - 100°


		# self.lower_blinker_hsv = np.uint8([180, 150, 220])  # 360° - 80°
		# self.upper_blinker_hsv = np.uint8([190, 220, 255])  # 360° - 100°


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
			t1_mean_filtering = datetime.now()
			# mean filter to reduce noise
			kernel = np.ones((6, 6), dtype=np.float32) / 36

			mean_filtered = opencv.filter2D(image, -1, kernel)
			t2_mean_filtering = datetime.now()

			# convert to HSV image
			# hsv_image = opencv.cvtColor(mean_filtered, opencv.COLOR_RGB2HSV)
			t1_hsv_image = datetime.now()
			hsv_image = opencv.cvtColor(mean_filtered, opencv.COLOR_BGR2HSV)
			t2_hsv_image = datetime.now()

			# HSV color segmentation
			t1_mask = datetime.now()
			mask_image = opencv.inRange(hsv_image, self.lower_blinker_hsv, self.upper_blinker_hsv)  # select only the pixels with HSV in the given range
			t2_mask = datetime.now()

			# closing to make segments compact
			t1_closing = datetime.now()
			kernel = self.create_kernel(rows=40, cols=40)
			closing_image = opencv.morphologyEx(mask_image, opencv.MORPH_CLOSE, kernel)
			t2_closing = datetime.now()

			# create border around the image to create "fair" conditions for each pixel in the closing and erode step
			t1_bordering = datetime.now()
			border_top = 3
			border_bottom = 3
			border_left = 3
			border_right = 3
			bordered_image = self.add_border(closing_image, border_top, border_bottom, border_left, border_right)
			t2_bordering = datetime.now()

			# erode to remove noise
			t1_erode = datetime.now()
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
			t2_erode = datetime.now()

			# set the result
			result_image = eroded_image

			self.processed_image_counter += 1
			if config_development_mode:
				print(self.processed_image_counter, 'images processed')

			# TODO: candidate for asyncIO???
			if config_development_mode:
				original_image_file_path = 'test_image_' + str(self.processed_image_counter) + '.PNG'
				hsv_image_file_path = 'test_image_hsv_' + str(self.processed_image_counter) + '.PNG'
				processed_image_file_path = 'test_image_eroded_' + str(self.processed_image_counter) + '.PNG'

				self.image_file_writer.write_images(
					original_image_file_path, image,
					hsv_image_file_path, hsv_image,
					processed_image_file_path, result_image
				)

			t1_search = datetime.now()
			
			if any(255 in x for x in result_image):
				t2_search = datetime.now()

				if config_development_mode:
					print('TIMINGS FOR PROCESSING:')
					print('TIME MEAN FILTERING: ', calculate_time_diff(t1_mean_filtering, t2_mean_filtering), 's', sep='')
					print('TIME HSV CONVERSION: ', calculate_time_diff(t1_hsv_image, t2_hsv_image), 's', sep='')
					print('TIME MASKING: ', calculate_time_diff(t1_mask, t2_mask), 's', sep='')
					print('TIME CLOSING: ', calculate_time_diff(t1_closing, t2_closing), 's', sep='')
					print('TIME BORDERING: ', calculate_time_diff(t1_bordering, t2_bordering), 's', sep='')
					print('TIME ERODING: ', calculate_time_diff(t1_erode, t2_erode), 's', sep='')
					print('TIME SEARCH FOR LABELS: ', calculate_time_diff(t1_search, t2_search), 's', sep='')

					print('found direction indicator')

				return ProcessedCameraData(probability=100.0, result=True)
			else:
				t2_search = datetime.now()
				
				if config_development_mode:
					print('TIMINGS FOR PROCESSING:')
					print('TIME MEAN FILTERING: ', calculate_time_diff(t1_mean_filtering, t2_mean_filtering), 's', sep='')
					print('TIME HSV CONVERSION: ', calculate_time_diff(t1_hsv_image, t2_hsv_image), 's', sep='')
					print('TIME MASKING: ', calculate_time_diff(t1_mask, t2_mask), 's', sep='')
					print('TIME CLOSING: ', calculate_time_diff(t1_closing, t2_closing), 's', sep='')
					print('TIME BORDERING: ', calculate_time_diff(t1_bordering, t2_bordering), 's', sep='')
					print('TIME ERODING: ', calculate_time_diff(t1_erode, t2_erode), 's', sep='')
					print('TIME SEARCH FOR LABELS: ', calculate_time_diff(t1_search, t2_search), 's', sep='')

					print('no direction indicator found')

				return ProcessedCameraData(probability=100.0, result=False)

def calculate_time_diff(t1, t2):
	return (t2 - t1).microseconds / (1*10**6) + (t2-t1).seconds
