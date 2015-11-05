import numpy as np
import cv2 as opencv
import sys

print('using OpenCV version:', opencv.__version__)

lower_blinker_hsv = np.uint8([80,150,220])
upper_blinker_hsv = np.uint8([100,200,255])

print('lower blinker hsv:', lower_blinker_hsv)
print('upper blinker hsv:', upper_blinker_hsv)

image_files_paths = [
	'1.jpeg',
	'2.jpeg',
	'3.jpeg',
	'4.jpeg',
	'5.jpeg',
	'6.jpeg',
	'7.jpeg',
	'8.png',
	'9.jpeg',
	'10.jpeg',
	'11.jpeg',
	'12.jpg',
	'13.JPG',
	'14.jpg',
	'15.jpg',
	'16.jpeg',
	'17.jpeg',
	'18.jpeg',
	'19.jpeg',
	'20.jpg',
	'21.jpg',
	'22.jpg',
	'23.jpg',
	'24.jpg',
	'25.jpg',
	'26.jpg',
	'27.jpg',
	'28.jpg',
	'29.jpg'
]

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
			opencv.imwrite(file_name, image_data, (opencv.IMWRITE_PNG_COMPRESSION, 0))
			index += 2

def main():
	for index, image_file_path in enumerate(image_files_paths):
		# read image file
		image = opencv.imread(image_file_path, -1)

		# eventuell schonmal runterskalieren
		# TODO

		# mean filter to reduce noise
		kernel = np.ones((6,6), dtype=np.float32)/36
		mean_filtered = opencv.filter2D(image, -1, kernel)

		# convert to HSV image
		hsv_image = opencv.cvtColor(mean_filtered, opencv.COLOR_RGB2HSV)  # convert to HSV image, V = 100, because RGB:255,255,255, checked with GIMP

		# HSV color segmentation
		mask_image = opencv.inRange(hsv_image, lower_blinker_hsv, upper_blinker_hsv)  # select only the pixels with HSV in the given range

		# opening, to eliminate noise
		# kernel = create_kernel(rows=5, cols=5)
		# opening_image = opencv.morphologyEx(mask_image, opencv.MORPH_OPEN, kernel)

		# create border around the image to create "fair" conditions for each pixel in the closing and erode step
		border_top = 3
		border_bottom = 3
		border_left = 3
		border_right = 3
		bordered_image = add_border(mask_image, border_top, border_bottom, border_left, border_right)

		# closing to make segments compact
		kernel = create_kernel(rows=30, cols=30)
		closing_image = opencv.morphologyEx(bordered_image, opencv.MORPH_CLOSE, kernel)

		# erode to remove noise
		kernel = create_kernel(rows=3, cols=3)
		eroded_image = opencv.erode(closing_image, kernel=kernel, iterations=3)

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

		# write_images(str(index+1) + '_written_step1_mean_filtered.png', mean_filtered)
		# write_images(str(index+1) + '_written_step2_hsv.png', hsv_image)
		# write_images(str(index+1) + '_written_step3_mask.png', mask_image)
		# write_images(str(index+1) + '_written_step4_opening.png', opening_image)
		# write_images(str(index+1) + '_written_step5_bordered.png', bordered_image)
		# write_images(str(index+1) + '_written_step6_closing.png', closing_image)
		# write_images(str(index+1) + '_written_step7_eroded.png', eroded_image)
		# write_images(str(index+1) + '_written_step8_result.png', result_image)
		write_images(str(index+1) + '_written_step9_masked_original.png', masked_original_image)

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
