import time
import sched
from datetime import datetime

import wiringpi2 as wiringpi
import picamera

# import enums
from model.WarningLevel import WarningLevel
from model.GPIOPin import GPIOPin
from model.PinMode import PinMode

# import classes
from adapter.CameraAdapter import CameraAdapter
from processor.CameraDataProcessor import CameraDataProcessor
from controller.LEDController import LEDController
from controller.SpeakerController import SpeakerController
from evaluator.SensorDataEvaluator import SensorDataEvaluator

# import helpers
from helper.TimeFunction import TimeFunction


__author__ = 'Hans-Werner Roitzsch'


class BikerApp:
	def __init__(self):
		self.initialize_hardware()

		self.camera_adapter = CameraAdapter()
		self.camera_data_processor = CameraDataProcessor()
		self.led_controller = LEDController()
		self.speaker_controller = SpeakerController()

		self.sensor_data_evaluator = SensorDataEvaluator()
		self.scheduler = sched.scheduler()  # default is time.monotonic and time.sleep
		self.emit_ready_signal_count = 0

		self.total_time_average = 0
		self.loop_iterations = 0

	def analyze_camera(self):
		t1_total = datetime.now()

		print('TIME:', datetime.now(), ': processing camera image ...')

		t1_get_image = datetime.now()
		camera_data = self.camera_adapter.get_data()
		t2_get_image = datetime.now()

		t1_process_image = datetime.now()
		processed_camera_data = self.camera_data_processor.process_data(camera_data)
		t2_process_image = datetime.now()

		t1_evaluate_result = datetime.now()
		self.sensor_data_evaluator.evaluate(processed_camera_data)
		t2_evaluate_result = datetime.now()

		t2_total = datetime.now()

		print('TIME TOTAL: ', TimeFunction.calculate_time_diff(t1_total, t2_total), 's', sep='')
		print('TIME GET IMAGE: ', TimeFunction.calculate_time_diff(t1_get_image, t2_get_image), 's', sep='')
		print('TIME PROCESSING: ', TimeFunction.calculate_time_diff(t1_process_image, t2_process_image), 's', sep='')
		print('TIME EVALUATE: ', TimeFunction.calculate_time_diff(t1_evaluate_result, t2_evaluate_result), 's', sep='')

	def initialize_hardware(self):
		wiringpi.wiringPiSetup()
		wiringpi.pinMode(GPIOPin.PIN_STATUS_LED.value, PinMode.OUTPUT.value)
		wiringpi.pinMode(GPIOPin.PIN_SOUND.value, PinMode.OUTPUT.value)
		wiringpi.pinMode(GPIOPin.PIN_RGB_RED.value, PinMode.OUTPUT.value)
		wiringpi.pinMode(GPIOPin.PIN_RGB_GREEN.value, PinMode.OUTPUT.value)
		wiringpi.pinMode(GPIOPin.PIN_RGB_BLUE.value, PinMode.OUTPUT.value)

	def emit_ready_signal(self):
		for run_count in range(3):
			wiringpi.digitalWrite(GPIOPin.PIN_STATUS_LED.value, GPIOPin.STATUS_HIGH.value)
			time.sleep(0.3)
			wiringpi.digitalWrite(GPIOPin.PIN_STATUS_LED.value, GPIOPin.STATUS_LOW.value)
			time.sleep(0.3)

	def run(self):
		self.emit_ready_signal()

		while True:
			self.analyze_camera()
			self.loop_iterations += 1

def main():
	app = BikerApp()
	app.run()

if __name__ == '__main__':
	main()
