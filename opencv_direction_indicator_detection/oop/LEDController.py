import wiringpi2 as wiringpi

from GPIOPin import GPIOPin
from PinMode import PinMode
from WarningLevel import WarningLevel

__author__ = 'Hans-Werner Roitzsch'

class LEDController(ActorController):
	def __init__():
		pass

	def start_warning(self, warning_level):
		if warning_level == WarningLevel.HAZARD_SPOT_WARNING:
			self.set_led_yellow()

		else if warning_level == WarningLevel.DANGEROUS_SITUATION_WARNING:
			self.set_led_red()

	def stop_warning(self):
		self.switch_off_leds()

	def set_led_red(self):
		self.switch_off_leds()
		self.set_pin(GPIOPin.PIN_RGB_RED, GPIOPin.STATUS_HIGH)

	def set_led_green(self):
		self.switch_off_leds()
		self.set_pin(GPIOPin.PIN_RGB_GREEN, GPIOPin.STATUS_HIGH)

	def set_led_blue(self):
		self.switch_off_leds()
		self.set_pin(GPIOPin.PIN_RGB_GREEN, GPIOPin.STATUS_HIGH)

	def set_led_yellow(self):
		self.switch_off_leds()
		self.set_pin(GPIOPin.PIN_RGB_GREEN, GPIOPin.STATUS_HIGH)


	def set_pin(self, gpio_pin, status):
		wiringpi.digitalWrite(gpio_pin, status)

	def switch_off_leds(self):
		wiringpi.digitalWrite(GPIOPin.PIN_RGB_RED, GPIOPin.STATUS_LOW)
		wiringpi.digitalWrite(GPIOPin.PIN_RGB_GREEN, GPIOPin.STATUS_LOW)
		wiringpi.digitalWrite(GPIOPin.PIN_RGB_BLUE, GPIOPin.STATUS_LOW)

# def switch_led_on():
# 	GPIO.output(LED_GPIO_PIN_NUMBER, True)  # switch it on!
# 	GPIO.cleanup()  # still necessary if I want to have the LED on?
#
#
# def switch_led_off():
# 	GPIO.output(LED_GPIO_PIN_NUMBER, False)  # switch it off!
# 	GPIO.cleanup()  # still necessary if I want to have the LED on?
