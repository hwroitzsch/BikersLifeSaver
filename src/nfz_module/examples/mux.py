import wiringpi2 as wiringpi
from time import sleep
import spidev

pin_status_low = 0
pin_status_high = 1

pin_mode_output = 1
pin_mode_input = 0

pin_a0 = 27
pin_a1 = 37
pin_en = 24
pin_sh = 38

reference_voltage = 2.5


#channels = [128, 144, 160, 176, 192, 208, 224, 240]
channels = [128]
spi = spidev.SpiDev()

def initialize_hardware():
	SPI_CHANNEL = 1
	SPI_SPEED = 100000
	
	wiringpi.wiringPiSetup()  # can be used like this: wiringpi.wiringPiSetup(SPI_CHANNEL, SPI_SPEED)
	wiringpi.pinMode(pin_a0, pin_mode_output)
	wiringpi.pinMode(pin_a1, pin_mode_output)
	wiringpi.pinMode(pin_en, pin_mode_output)

def calculate_voltage(spi_pin_data):
	return ((spi_pin_data[1] * 256) + spi_pin_data[2]) * (reference_voltage / 1024)
	
def get_data_from_spi_bus(channel):
	return spi.xfer([1, channel, 0])

def main():
	initialize_hardware()

	wiringpi.digitalWrite(pin_a0, pin_status_low)
	wiringpi.digitalWrite(pin_a1, pin_status_low)
	wiringpi.digitalWrite(pin_en, pin_status_high)
	
	bus = 0
	device = 1
	spi.open(bus, device)

	counter = 0
	values = []
	
	while len(values) < 600:
		for index, channel in enumerate(channels):
			spi_pin_data = get_data_from_spi_bus(channel)
			
			if 0 <= spi_pin_data[1] <= 3:  # check if undefined value
				voltage = calculate_voltage(spi_pin_data)
				values.append(voltage)
			
		wiringpi.digitalWrite(pin_sh, pin_status_low)
		counter += 1

	index = 0
	step = 10
	while index < len(values):
		for i in range(step):
			print('${0:.5f}'.format(values[index * step + i]), end='  ')
		index += step

if __name__ == '__main__':
	main()
