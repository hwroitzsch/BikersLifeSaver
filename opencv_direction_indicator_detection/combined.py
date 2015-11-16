import time
import sched
import datetime
import picamera
import picamera.array
import cv2 as opencv
import numpy as np
import RPi.GPIO as GPIO

IMAGE_WIDTH = 1024
IMAGE_HEIGHT = 768

lower_blinker_hsv = np.uint8([80,150,220])
upper_blinker_hsv = np.uint8([100,220,255])

LED_GPIO_PIN_NUMBER = 7
GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(LED_GPIO_PIN_NUMBER, GPIO.OUT) ## Setup GPIO Pin to OUT

print('using OpenCV version:', opencv.__version__)


def get_image_from_camera():
    with picamera.PiCamera() as camera:
        camera.resolution = (IMAGE_WIDTH, IMAGE_HEIGHT)
        camera.framerate = 24
        time.sleep(2)

        with picamera.array.PiRGBArray(camera) as stream:
            camera.start_preview()
            camera.capture(stream, format='rgb')
            return stream.array


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


def switch_led_on():
    GPIO.output(LED_GPIO_PIN_NUMBER, True)  # switch it on!
    GPIO.cleanup()  # still necessary if I want to have the LED on?


def switch_led_off():
    GPIO.output(LED_GPIO_PIN_NUMBER, False)  # switch it off!
    GPIO.cleanup()  # still necessary if I want to have the LED on?

    
def process_images():
    image = get_image_from_camera()
    if image.shape is not None:
        # mean filter to reduce noise
        kernel = np.ones((6,6), dtype=np.float32)/36
        mean_filtered = opencv.filter2D(image, -1, kernel)

        # convert to HSV image
        hsv_image = opencv.cvtColor(mean_filtered, opencv.COLOR_RGB2HSV)

        # HSV color segmentation
        mask_image = opencv.inRange(hsv_image, lower_blinker_hsv, upper_blinker_hsv)  # select only the pixels with HSV in the given range

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
        eroded_image = remove_border(eroded_image, border_top, border_bottom, border_left, border_right)

        # set the result
        result_image = eroded_image

        if any(255 in x for x in result_image):
            switch_led_on()
            pass
        else:
            switch_led_off()
            pass
    
def main():
    scheduler = sched.scheduler(time.time, time.sleep)

    def do_something(scheduler):
        print('TIME:', datetime.datetime.now())
        scheduler.enter(1, 1, do_something, (scheduler,))

    scheduler.enter(1, 1, do_something, (scheduler,))
    scheduler.run()
    

if __name__ == '__main__':
    main()
