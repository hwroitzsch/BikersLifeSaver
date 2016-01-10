__author__ = 'Hans-Werner Roitzsch'


import os, sys
import numpy as np
import cv2 as opencv


allowed_formats = ['png', 'jpg', 'jpeg']


class LabelCounting:
	def __init__(self):
		self.label_count = 0

	def count_labels(self, masked_image):
		contours = opencv.findContours(masked_image, mode=opencv.RETR_LIST, method=opencv.CHAIN_APPROX_NONE)
		print('=====CONTOURS=====')
		print(countour)
		return len(contours)







def get_file_ending(file_name):
	dot_pos = file_name.rfind('.')
	if dot_pos != -1:
		return file_name[dot_pos+1:]
	return None

def get_image_file_paths(image_dir):
	"""This method searches for file names of images of allowed formats in the given directory."""
	result = []

	path = os.getcwd()
	if image_directory != '':
		path = os.path.join(os.getcwd(), image_dir)

	file_names_in_directory = os.listdir(path)

	only_files = [
		name for name in file_names_in_directory if os.path.isfile(os.path.join(path, name))
	]

	only_image_file_names = [
		name for name in only_files if any(
			ending.lower() in get_file_ending(name) for ending in allowed_formats
		)
	]

	full_paths = []
	for name in only_image_file_names:
		full_paths.append(os.path.join(path, name))

	print('ALL IMAGE FILES:', full_paths)

	return only_image_file_paths

def load_image(image_file_path):
	print('Loading image from:', image_file_path)
	return opencv.imread(image_file_path, -1)

def main():
	image_directory = sys.argv[1]
	print('Given image directory:', image_directory)
	
	image_file_paths = get_image_file_paths(image_directory)

	label_counter = LabelCounting()
	
	for image_file_path in image_file_paths:
		labels_count = label_counter.count_labels(load_image(image_file_path))
		print('Image', image_file_paths, 'has', labels_count, 'labels.')

if __name__ == '__main__':
	main()