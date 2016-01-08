import gps as gps3
from gps import WATCH_ENABLE, WATCH_NEWSTYLE
# from gps import gps as gps3
# from gps import WATCH_ENABLE, WATCH_NEWSTYLE

# Listen on port 2947 (gpsd) of localhost
print('gps3:')
print(dir(gps3))

print('gps3.gps:')
print(dir(gps3.gps))

session = gps3.gps("localhost", "2947")
session.stream(WATCH_ENABLE | WATCH_NEWSTYLE)

while True:
	try:
		report = session.next()
		# Wait for a 'TPV' report and display the current time
		# To see all report data, uncomment the line below
		# print report
		if report['class'] == 'TPV':
			if hasattr(report, 'time'):
				print('TIME:', report.time)

	except KeyError:
		pass

	except KeyboardInterrupt:
		quit()

	except StopIteration:
		session = None
		print("GPSD has terminated")
