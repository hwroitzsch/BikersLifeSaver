from enum import Enum

__author__ = 'Hans-Werner Roitzsch'

class GPIOPin(Enum):
	PIN_SOUND = 0
	PIN_STATUS_LED = 2
	PIN_RGB_RED = 3
	PIN_RGB_GREEN = 4
	PIN_RGB_BLUE = 5

	STATUS_HIGH = 1
	STATUS_LOW = 0
