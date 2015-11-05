import numpy as np
import cv2 as opencv
import sys

print('using OpenCV version:', opencv.__version__)

lower_blinker_hsv = np.uint8([90,210,190])
upper_blinker_hsv = np.uint8([96,230,255])

print('lower blinker hsv:', lower_blinker_hsv)
print('upper blinker hsv:', upper_blinker_hsv)

# imread:
# >0 --> 3 channels
# <0 --> as it is, even with alpha if it has alpha channel
# =0 --> grayscale
#image = opencv.imread('white.png', -1)

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
	'11.jpeg'
]

def create_kernel(rows=3, cols=3):
	return np.ones((rows, cols), dtype=np.int)

for index, image_file_path in enumerate(image_files_paths):
	image = opencv.imread(image_file_path, -1)
	hsv_image = opencv.cvtColor(image, opencv.COLOR_RGB2HSV)  # convert to HSV image, V = 100, because RGB:255,255,255, checked with GIMP
	mask = opencv.inRange(hsv_image, lower_blinker_hsv, upper_blinker_hsv)  # select only the pixels with HSV in the given range

	# closing to make segments compact
	kernel = create_kernel(rows=10, cols=10)
	closing = opencv.morphologyEx(mask, opencv.MORPH_CLOSE, kernel)

	# erode to remove noise
	kernel = create_kernel(rows=3, cols=3)
	eroded = opencv.erode(closing, kernel=kernel, iterations=2)


	result = eroded
	if any(255 in x for x in result):
		print(image_files_paths[index], str(index+1), 'Blinker color detected.')

	opencv.imwrite(str(index+1) + '_written_hsv.png', hsv_image, (opencv.IMWRITE_PNG_COMPRESSION, 9))
	opencv.imwrite(str(index+1) + '_written_mask.png', mask, (opencv.IMWRITE_PNG_COMPRESSION, 9))
	opencv.imwrite(str(index+1) + '_written_closing.png', closing, (opencv.IMWRITE_PNG_COMPRESSION, 9))
	opencv.imwrite(str(index+1) + '_written_eroded.png', eroded, (opencv.IMWRITE_PNG_COMPRESSION, 9))

# print('HSV image:')
# print(hsv_image)
# print('Mask:')
# print(mask)
# print(image)

# convert RGB to HSV values, can work on numpy arrays
#hsv_green = opencv.cvtColor(green, opencv.COLOR_BGR2HSV)
#print(hsv_green)


# If you can't find key CV_XXXXX in the cv2 module:
# cv2.XXXXX
# cv2.cv.CV_XXXXX
# For example: cv2.cv.CV_IMWRITE_PNG_COMPRESSION.
# Also check: http://stackoverflow.com/questions/9661512/python-opencv-imwrite-cant-find-params


# Good values: np.array([90,180,180]), np.array([100,255,255])
