from GPSController import GPSController

import time

if __name__ == '__main__':
	# create the controller
	gpsc = GPSController()
	try:
		# start controller
		gpsc.start()
		counter = 0
		while True:
			print('Counter:', counter)
			print('latitude:', gpsc.fix.latitude)
			print('longitude:', gpsc.fix.longitude)
			print('time utc:', gpsc.utc, ' + ', gpsc.fix.time)
			print('altitude (m):', gpsc.fix.altitude)
			print('eps:', gpsc.fix.eps)
			print('epx:', gpsc.fix.epx)
			print('epv:', gpsc.fix.epv)
			print('ept:', gpsc.gpsd.fix.ept)
			print('speed (m/s):', gpsc.fix.speed)
			print('climb:', gpsc.fix.climb)
			print('track:', gpsc.fix.track)
			print('mode:', gpsc.fix.mode)
			print('sats:', gpsc.satellites)
			time.sleep(0.5)
			counter += 1

	#Ctrl C
	except KeyboardInterrupt:
		print("User cancelled")

	#Error
	except:
		print("Unexpected error:", sys.exc_info()[0])
		raise

	finally:
		print("Stopping gps controller")
		gpsc.stopController()
		#wait for the tread to finish
		gpsc.join()

	print("Done")