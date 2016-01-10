__author__ = 'Hans-Werner Roitzsch'

import os
import numpy as np
import cv2 as opencv


class ImageReader:
	def __init__(self):
		self.images_directory = 'captured_images'
		self.images_file_paths = self.get_file_names()
		self.current_index = 0
		self.allowed_formats = ['jpg', 'jpeg', 'png']

	def get_file_names(self):
		"""This method searches for file names of images of allowed formats in the given directory."""
		result = []

		path = os.getcwd()
		if self.images_directory:
			path = os.path.join(os.getcwd(), self.images_directory)

		onlyfiles = [
			name for name in os.listdir(path) if (
				os.path.isfile(os.path.join(path, name)) and
				any(ending.lower() in name.lower() for ending in self.allowed_formats)
			)
		]
		print('ALL FILES:', onlyfiles)

		for file_name in onlyfiles:
			if 'hsv' in file_name:
				result.append(os.path.join(path, file_name))

		return result

	def read_next(self):
		"""This method reads the next image from the image directory."""
		image = opencv.imread(self.images_file_paths[self.current_index % len(self.images_file_paths)], -1)
		self.current_index += 1
		return image

