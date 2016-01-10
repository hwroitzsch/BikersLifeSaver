import time
import picamera
import picamera.array
import cv2 as opencv

IMAGE_WIDTH = 800
IMAGE_HEIGHT = 600

def main():
    with picamera.PiCamera() as camera:
        camera.resolution = (IMAGE_WIDTH, IMAGE_HEIGHT)
        camera.framerate = 24

        time.sleep(2)

        with picamera.array.PiRGBArray(camera) as stream:
            camera.start_preview()
            # camera.capture(stream, format='bgr')
            camera.capture(stream, format='rgb', use_video_port=True)
            # rgb_image = opencv.cvtColor(stream.array, opencv.COLOR_BGR2RGB)
            rgb_image = stream.array
            hsv_image = opencv.cvtColor(stream.array, opencv.COLOR_BGR2HSV)
            # At this point the image is available as stream.array
            # image_data = stream.array  # this is a BGR image
            opencv.imwrite('example_rgb.PNG', rgb_image, (opencv.IMWRITE_PNG_COMPRESSION, 0))
            opencv.imwrite('example_hsv.PNG', hsv_image, (opencv.IMWRITE_PNG_COMPRESSION, 0))

if __name__ == '__main__':
    main()
