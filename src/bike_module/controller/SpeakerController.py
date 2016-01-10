import wiringpi2 as wiringpi

from model.GPIOPin import GPIOPin
from model.PinMode import PinMode

from model.WarningLevel import WarningLevel
from controller.ActorController import ActorController

__author__ = 'Hans-Werner Roitzsch'


class SpeakerController(ActorController):
	def __init__(self):
		self.frequenzy = 3500
		self.stop_frequency = 0

	def start_warning(self, warning_level):
		print('starting warning')
		if warning_level == WarningLevel.DANGEROUS_SITUATION_WARNING.value:
			wiringpi.softToneCreate(GPIOPin.PIN_SOUND.value)
			wiringpi.softToneWrite(GPIOPin.PIN_SOUND.value, self.frequenzy)

	def stop_warning(self):
		print('stopping warning')
		wiringpi.softToneCreate(GPIOPin.PIN_SOUND.value)
		wiringpi.softToneWrite(GPIOPin.PIN_SOUND.value, self.stop_frequency)
