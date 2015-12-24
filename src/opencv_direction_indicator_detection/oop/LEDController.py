import wiringpi2 as wiringpi

from GPIOPin import GPIOPin
from PinMode import PinMode

from WarningLevel import WarningLevel
from ActorController import ActorController

__author__ = 'Hans-Werner Roitzsch'


class LEDController(ActorController):
	def __init__(self):
		pass

	def start_warning(self, warning_level):
		if warning_level == WarningLevel.HAZARD_SPOT_WARNING.value:
			self.set_led_yellow()

		elif warning_level == WarningLevel.DANGEROUS_SITUATION_WARNING.value:
			self.set_led_red()

	def stop_warning(self):
		self.switch_off_leds()

	def set_led_red(self):
		self.switch_off_leds()
		self.set_pin(GPIOPin.PIN_RGB_RED.value, GPIOPin.STATUS_HIGH.value)

	def set_led_green(self):
		self.switch_off_leds()
		self.set_pin(GPIOPin.PIN_RGB_GREEN.value, GPIOPin.STATUS_HIGH.value)

	def set_led_blue(self):
		self.switch_off_leds()
		self.set_pin(GPIOPin.PIN_RGB_GREEN.value, GPIOPin.STATUS_HIGH.value)

	def set_led_yellow(self):
		self.switch_off_leds()
		self.set_pin(GPIOPin.PIN_RGB_GREEN.value, GPIOPin.STATUS_HIGH.value)

	def set_pin(self, gpio_pin, status):
		wiringpi.digitalWrite(gpio_pin, status)

	def switch_off_leds(self):
		wiringpi.digitalWrite(GPIOPin.PIN_RGB_RED.value, GPIOPin.STATUS_LOW.value)
		wiringpi.digitalWrite(GPIOPin.PIN_RGB_GREEN.value, GPIOPin.STATUS_LOW.value)
		wiringpi.digitalWrite(GPIOPin.PIN_RGB_BLUE.value, GPIOPin.STATUS_LOW.value)

# def switch_led_on():
# 	GPIO.output(LED_GPIO_PIN_NUMBER, True)  # switch it on!
# 	GPIO.cleanup()  # still necessary if I want to have the LED on?
#
#
# def switch_led_off():
# 	GPIO.output(LED_GPIO_PIN_NUMBER, False)  # switch it off!
# 	GPIO.cleanup()  # still necessary if I want to have the LED on?
