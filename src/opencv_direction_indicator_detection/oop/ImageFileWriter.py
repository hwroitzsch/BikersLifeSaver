import sys
import os
import cv2 as opencv

class ImageFileWriter:
	def __init__(self):
		pass

	def write_images(self, *args):
		image_directory = '/root/ghisallo_venv/src/opencv_direction_indicator_detection/oop/test_images/'
		if len(args) % 2 != 0:
			print('argument error: got not enough names for files to write.')
		else:
			# save all images with their given names
			index = 0
			while index < len(args):
				file_name = args[index+0]
				image_data = args[index+1]
				file_path = os.path.join(image_directory, file_name)
				print('writing image file to', file_path)

				if image_data.shape is not None:
					converted_image_data = opencv.cvtColor(image_data, opencv.COLOR_RGB2BGR)  # images might need to be converted to be correctly written by opencv
				else:
					print('image_data.shape is None')
					
				opencv.imwrite(file_path, converted_image_data, (opencv.IMWRITE_PNG_COMPRESSION, 0))
				index += 2
