import wiringpi2 as wiringpi

from GPIOPin import GPIOPin
from PinMode import PinMode
from WarningLevel import WarningLevel

__author__ = 'Hans-Werner Roitzsch'

class SpeakerController(ActorController):
	def __init__(self):
		self.frequenzy = 3500

	def start_warning(self, warning_level):
		if warning_level == WarningLevel.DANGEROUS_SITUATION_WARNING:
			wiringpi.softToneCreate(GPIOPin.PIN_SOUND)
			wiringpi.softToneWrite(GPIOPin.PIN_SOUND, self.frequenzy)
