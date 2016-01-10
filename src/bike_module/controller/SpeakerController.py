__author__ = 'Hans-Werner Roitzsch'


import wiringpi2 as wiringpi

from model.GPIOPin import GPIOPin
from model.PinMode import PinMode

from model.WarningLevel import WarningLevel
from controller.ActorController import ActorController

import config
import time
import sched

class SpeakerController(ActorController):
	def __init__(self):
		self.frequenzy = 3500
		self.stop_frequency = 0
		self.scheduler = sched.scheduler()

	def start_warning(self, warning_level):
		if config.development_mode:
			print('starting warning')

		if warning_level == WarningLevel.DANGEROUS_SITUATION_WARNING.value:
			wiringpi.softToneCreate(GPIOPin.PIN_SOUND.value)
			wiringpi.softToneWrite(GPIOPin.PIN_SOUND.value, self.frequenzy)

			# schedule stop warning
			self.scheduler.enter(0, 1, self.stop_after_duration, argument=(2))
			self.scheduler.run(blocking=False)

	def stop_warning(self):
		if config.development_mode:
			print('stopping warning')

		wiringpi.softToneCreate(GPIOPin.PIN_SOUND.value)
		wiringpi.softToneWrite(GPIOPin.PIN_SOUND.value, self.stop_frequency)

	def stop_after_duration(self, duration):
		time.sleep(duration)
		self.stop_warning()