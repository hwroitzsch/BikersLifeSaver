import sys
import os
import cv2 as opencv

class ImageFileWriter:
	def __init__(self):
		pass

	def write_images(self, *args):
		image_directory = 'test_images/'
		if len(args) % 2 != 0:
			print('argument error: got not enough names for files to write.')
		else:
			# save all images with their given names
			index = 0
			while index < len(args):
				file_name = args[index+0]
				image_data = args[index+1]
				opencv.imwrite(os.path.join(image_directory, file_name), image_data, (opencv.IMWRITE_JPEG_QUALITY, 100))
				index += 2
