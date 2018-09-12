import socket
import sys
import os
import gps
import time
import select

initialized = False

service = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

queue = []
try:
	service.connect(('', 12344))
except ConnectionRefusedError:
	print("Server is down")
	sys.exit()

session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

print("Sending Current location data continously...")
sys.stdout.write('Command: ')
sys.stdout.flush()
while True:
	readable, _, _ = select.select([sys.stdin], [], [], 0)
	try:
		if sys.stdin in readable:
			queue.insert(0, str(sys.stdin.readline()).encode('ascii'))
			time.sleep(0.5)
			sys.stdout.write('Command: ')
			sys.stdout.flush()
		else:
			report = session.next()
			if report['class']=='TPV':
				if hasattr(report, 'time') and hasattr(report, 'lon') and hasattr(report, 'lat'):
					# print('Time: {}\nPosition: {} N {} E\n'.format(report.time, report.lon, report.lat))
					if  not initialized:
						queue.insert(0, str("INIT "+str(report.lon)+" "+str(report.lat)).encode('ascii'))
						initialized=True
					else:
						service.send(str("CURRENT "+str(report.lon)+" "+str(report.lat)).encode('ascii'))
		while len(queue) > 0:
			service.send(queue.pop())
			time.sleep(0.5) 
	except Exception as e:
		print(e)
	except KeyboardInterrupt:
		print("Exiting!")
		service.close()
		sys.exit()

