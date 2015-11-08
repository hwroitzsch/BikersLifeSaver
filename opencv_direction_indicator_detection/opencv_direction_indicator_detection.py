import numpy as np
import cv2 as opencv
import sys
import os

print('using OpenCV version:', opencv.__version__)

image_directory = 'direction_indicator_active_night/'
# image_directory = 'direction_indicator_active_web/'
# image_directory = 'direction_indicator_inactive_night/'

allowed_formats = ['png', 'jpg', 'jpeg']

# correctly detected active : 40 of 70
# not detected active: 30 of 70
# false positives: 3 of 103
lower_blinker_hsv = np.uint8([80,150,220])
upper_blinker_hsv = np.uint8([100,220,255])

# correctly detected active : 58 of 70
# not detected active: 12 of 70
# false positives: 46 of 103
# lower_blinker_hsv = np.uint8([80,100,220])
# upper_blinker_hsv = np.uint8([100,220,255])

print('lower blinker hsv:', lower_blinker_hsv)
print('upper blinker hsv:', upper_blinker_hsv)

image_files_paths = []

def create_kernel(rows=3, cols=3):
	return np.ones((rows, cols), dtype=np.int)

def print_rows_cols(image):
	rows_and_cols = image.shape
	print('Rows and cols:', rows_and_cols)

def add_border(image, top, bottom, left, right, color=0):
	return opencv.copyMakeBorder(
		image,
		top, bottom, left, right,
		opencv.BORDER_CONSTANT,
		value=color
	)

def remove_border(image, top, bottom, left, right):
	rows_and_cols = image.shape
	return image[top:rows_and_cols[0]-bottom, left:rows_and_cols[1]-right]

def write_images(*args):
	if len(args) % 2 != 0:
		print('argument error: got not enough names for files to write.')
	else:
		# save all images with their given names
		index = 0
		while index < len(args):
			file_name = args[0]
			image_data = args[1]
			opencv.imwrite(os.path.join(image_directory, file_name), image_data, (opencv.IMWRITE_PNG_COMPRESSION, 0))
			index += 2

def get_file_ending(file_name):
	dot_pos = file_name.rfind('.')
	if dot_pos != -1:
		return file_name[dot_pos+1:]
	return None

def get_file_names(image_dir):
	"""This method searches for file names of images of allowed formats in the given directory."""
	result = []

	path = os.getcwd()
	if image_directory != '':
		path = os.path.join(os.getcwd(), image_dir)

	onlyfiles = [
		name for name in os.listdir(path) if (
			os.path.isfile(os.path.join(path, name)) and
			any(ending.lower() in name.lower() for ending in allowed_formats)
		)
	]
	print('ALL FILES:', onlyfiles)

	for file_name in onlyfiles:
		if 'written' not in file_name:
			result.append(os.path.join(path, file_name))

	return result

def main():
	image_files_paths = get_file_names(image_directory)
	detected_counter = 0
	not_detected_counter = 0

	for index, image_file_path in enumerate(image_files_paths):
		# read image file
		image = opencv.imread(image_file_path, -1)

		if image.shape is not None:

			# eventuell schonmal runterskalieren
			# TODO

			# mean filter to reduce noise
			kernel = np.ones((6,6), dtype=np.float32)/36
			mean_filtered = opencv.filter2D(image, -1, kernel)

			# convert to HSV image
			hsv_image = opencv.cvtColor(mean_filtered, opencv.COLOR_RGB2HSV)
			# try:
			# 	hsv_image = opencv.cvtColor(mean_filtered, opencv.IMREAD_ANYCOLOR)


			# HSV color segmentation
			mask_image = opencv.inRange(hsv_image, lower_blinker_hsv, upper_blinker_hsv)  # select only the pixels with HSV in the given range

			# opening, to eliminate noise
			# kernel = create_kernel(rows=5, cols=5)
			# opening_image = opencv.morphologyEx(mask_image, opencv.MORPH_OPEN, kernel)

			# closing to make segments compact
			kernel = create_kernel(rows=40, cols=40)
			closing_image = opencv.morphologyEx(mask_image, opencv.MORPH_CLOSE, kernel)

			# create border around the image to create "fair" conditions for each pixel in the closing and erode step
			border_top = 3
			border_bottom = 3
			border_left = 3
			border_right = 3
			bordered_image = add_border(closing_image, border_top, border_bottom, border_left, border_right)

			# erode to remove noise
			kernel = create_kernel(rows=3, cols=3)
			eroded_image = opencv.erode(bordered_image, kernel=kernel, iterations=3)

			# remove border for bitwise AND operation with original image
			rows_and_cols = eroded_image.shape
			eroded_image = remove_border(eroded_image, border_top, border_bottom, border_left, border_right)

			# set the result
			result_image = eroded_image

			# which areas of the original image have been detected as direction indicator?
			# AND operation with the result and original image
			# The original image's values are only shown when the result has a brightness value of 255.
			masked_original_image = opencv.bitwise_and(image, image, mask=result_image)


			if any(255 in x for x in result_image):
				print(image_files_paths[index], 'Blinker color detected.')
				detected_counter += 1
			else:
				not_detected_counter += 1


			write_images(os.path.split(image_file_path)[1] + '_' + str(index+1) + '_written_step1_mean_filtered.png', mean_filtered)
			write_images(os.path.split(image_file_path)[1] + '_' + str(index+1) + '_written_step2_hsv.png', hsv_image)
			write_images(os.path.split(image_file_path)[1] + '_' + str(index+1) + '_written_step3_mask.png', mask_image)
			# write_images(os.path.split(image_file_path)[1] + '_' + str(index+1) + '_written_step4_opening.png', opening_image)
			write_images(os.path.split(image_file_path)[1] + '_' + str(index+1) + '_written_step5_closing.png', closing_image)
			write_images(os.path.split(image_file_path)[1] + '_' + str(index+1) + '_written_step6_bordered.png', bordered_image)
			write_images(os.path.split(image_file_path)[1] + '_' + str(index+1) + '_written_step7_eroded.png', eroded_image)
			write_images(os.path.split(image_file_path)[1] + '_' + str(index+1) + '_written_step8_result.png', result_image)
			write_images(os.path.split(image_file_path)[1] + '_' + str(index+1) + '_written_step9_masked_original.png', masked_original_image)

		print('Images analysed:', len(image_files_paths))
		print('Direction indicator detected in', detected_counter, 'images.')
		print('Direction indicator not detected in', not_detected_counter, 'images.')

if __name__ == '__main__':
	main()

# If you can't find key CV_XXXXX in the cv2 module:
# cv2.XXXXX
# cv2.cv.CV_XXXXX
# For example: cv2.cv.CV_IMWRITE_PNG_COMPRESSION.
# Also check: http://stackoverflow.com/questions/9661512/python-opencv-imwrite-cant-find-params
# import cv2
# nms = dir(cv2) # list of everything in the cv2 module
# [m for m in nms if 'MORPH' in m]

# imread:
# >0 --> 3 channels
# <0 --> as it is, even with alpha if it has alpha channel
# =0 --> grayscale
#image = opencv.imread('white.png', -1)
