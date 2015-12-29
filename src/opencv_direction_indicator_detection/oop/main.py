import time
import sched
from datetime import datetime

import config

import wiringpi2 as wiringpi
import picamera

# import enums
from WarningLevel import WarningLevel
from GPIOPin import GPIOPin
from PinMode import PinMode

# import classes
from CameraAdapter import CameraAdapter
from CameraDataProcessor import CameraDataProcessor
from LEDController import LEDController
from SpeakerController import SpeakerController
from SensorDataEvaluator import SensorDataEvaluator

__author__ = 'Hans-Werner Roitzsch'


class BikerApp:

	def __init__(self):
		self.initialize_hardware()

		self.camera_adapter = CameraAdapter()
		self.camera_data_processor = CameraDataProcessor()
		self.led_controller = LEDController()
		self.speaker_controller = SpeakerController()

		self.sensor_data_evaluator = SensorDataEvaluator()

	def analyze_camera(self):
		print('TIME:', datetime.now(), ': processing camera image ...')
		camera_data = self.camera_adapter.get_data()
		processed_camera_data = self.camera_data_processor.process_data(camera_data)
		self.sensor_data_evaluator.evaluate(processed_camera_data)

	def analyze_hazard_spots(self):
		print('TIME:', datetime.now(), ': processing hazard spot data ...')
		# TODO:
		# get hazard_spot data from server using the network communicator
		# get gps data from gps mouse using a GPSMouseAdapter (not yet written)
		# compare data and determin whether or not we are at a hazard spot
		# if we are at a hazard spot, give an appropriate warning
		pass

	def initialize_hardware(self):
		wiringpi.wiringPiSetup()
		wiringpi.pinMode(GPIOPin.PIN_STATUS_LED.value, PinMode.OUTPUT.value)
		wiringpi.pinMode(GPIOPin.PIN_SOUND.value, PinMode.OUTPUT.value)
		wiringpi.pinMode(GPIOPin.PIN_RGB_RED.value, PinMode.OUTPUT.value)
		wiringpi.pinMode(GPIOPin.PIN_RGB_GREEN.value, PinMode.OUTPUT.value)
		wiringpi.pinMode(GPIOPin.PIN_RGB_BLUE.value, PinMode.OUTPUT.value)

	def run(self):
		task_priority = 1
		run_count = 1  # run_count is only 1 but it'll be used over and over again
		scheduler = sched.scheduler()  # default is time.monotonic and time.sleep

		def do_something(scheduler):
			self.analyze_camera()
			scheduler.enter(run_count, task_priority, do_something, (scheduler,))

		scheduler.enter(run_count, task_priority, do_something, (scheduler,))
		scheduler.run()

		# for more details about the scheduler take a look at:
		# https://docs.python.org/3/library/sched.html#sched.scheduler


def main():
	app = BikerApp()
	app.run()

if __name__ == '__main__':
	main()
