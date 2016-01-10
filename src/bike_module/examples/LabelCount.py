__author__ = 'Hans-Werner Roitzsch'


import os, sys
import numpy as np
import cv2 as opencv
from scipy import ndimage
from datetime import datetime

from TimeFunction import TimeFunction

allowed_formats = ['png', 'jpg', 'jpeg']


# lower_blinker_hsv = np.uint8([260, 150, 220])
# upper_blinker_hsv = np.uint8([280, 220, 255])


class LabelCounting:
	def __init__(self):
		self.label_count = 0

	def count_labels(self, image):
		t1_get_label_count = datetime.now()
		label_im, nb_labels = ndimage.label(image)
		t2_get_label_count = datetime.now()
		print('COUNTING OF LABELS TOOK:', TimeFunction.calculate_time_diff(t1_get_label_count, t2_get_label_count), 's', sep='')
		print('COUNT OF LABELS:', nb_labels)

		return nb_labels


def pre_process_image(image):
	hsv_image = opencv.cvtColor(image, opencv.COLOR_BGR2HSV)
	mask_image = opencv.inRange(hsv_image, lower_blinker_hsv, upper_blinker_hsv)  # select only the pixels with HSV in the given range
	return mask_image

def get_file_ending(file_name):
	dot_pos = file_name.rfind('.')
	if dot_pos != -1:
		return file_name[dot_pos+1:]
	return None

def get_image_file_paths(image_dir):
	"""This method searches for file names of images of allowed formats in the given directory."""
	result = []

	file_names_in_directory = os.listdir(image_dir)

	print('ALL FILES IN DIR:', file_names_in_directory)

	only_files = [
		name for name in file_names_in_directory if os.path.isfile(os.path.join(image_dir, name))
	]

	print('ONLY FILES:', only_files)

	only_image_file_names = [
		name for name in only_files if any(
			ending.lower() in get_file_ending(name) for ending in allowed_formats
		)
	]

	only_image_file_paths = [os.path.join(image_dir, name) for name in only_image_file_names]

	print('ALL IMAGE FILES:', only_image_file_paths)

	return only_image_file_paths

def load_image(image_file_path):
	print('Loading image from:', image_file_path)
	return opencv.imread(image_file_path, -1)

def save_image(image_data, image_file_path):
	print('writing image file to', image_file_path)
	opencv.imwrite(image_file_path, image_data, (opencv.IMWRITE_PNG_COMPRESSION, 0))

def main():
	image_directory = sys.argv[1]
	print('Given image directory:', image_directory)
	
	image_file_paths = get_image_file_paths(image_directory)

	label_counter = LabelCounting()
	
	for index, image_file_path in enumerate(image_file_paths):
		image = load_image(image_file_path)
		# image = pre_process_image(image)
		
		# if image is not None:
		# 	print('Image shape:', image.shape)
		# 	save_image(image, os.path.join(image_directory, 'pre_processed_image_' + str(index) + '.png'))
		# else:
		# 	print('Image was None.')

		labels_count = label_counter.count_labels(image)
		print('Image', image_file_path, 'has', labels_count, 'labels.')


# def calculate_time_diff(t1, t2):
	# return (t2 - t1).microseconds / (1 * 10**6) + (t2 - t1).seconds

if __name__ == '__main__':
	main()