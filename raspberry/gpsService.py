import socket
import sys
import os
import gps
import time
import select
import argparse

# Buffer length
BUFFER = 1024

# =========
# Variables
# =========
isAuto = False
initialized = False
queue = []
location=[]
currentLocation=None
nextLocation=None
lastCommand=''
msg=''

# ========
# Sys Args
# ========
parser = argparse.ArgumentParser(description='Connect to Server')
parser.add_argument('hostname', type=str)
parser.add_argument('port', type=int)

args = parser.parse_args()

# ==========
# GPS Socket
# ==========
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

# =============
# Custom Scoket
# =============
HOST = args.hostname
PORT = args.port
service = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to station
try:
	service.connect((HOST, PORT))
except Exception as e:
	print("Station Server is down")
	sys.exit()


print("Sending Current location data continously...")

def parseCommand(data):
	operation=data[0]
	if operation == 'CLEAR':
		location=[]
		location.append(currentLocation)
		msg="[-] CLEARED LOCATION"
	elif operation=='ADD':
		if len(data) < 3:
			msg = 'Location not given properly!'
			return
		location.append([data[0], data[1]])
		msg='[+] Location Appended!'
	# TODO: Add condition to delete location by index
	else:
		msg='Unknown Data: ', str(data)

while True:
	readable, _, _ = select.select([service], [], [], 0)
	try:
		# If station is sending data, Execute it
		if service in readable:
			data = service.recv(BUFFER)
			if not data:
				service.close()
				print("Server closed the connection!")
				sys.exit()
			else:
				print("Recieved: ", data.decode('ascii'))
				parseCommand(data.decode('ascii').rstrip().split(' '))
		# Else send current location info
		else:
			report = session.next()
			if report['class']=='TPV' and not isAuto:
				if hasattr(report, 'time') and hasattr(report, 'lon') and hasattr(report, 'lat'):
					# print('Time: {}\nPosition: {} N {} E\n'.format(report.time, report.lon, report.lat))
					if  not initialized:
						currentLocation=[report.lon, report.lat]
						queue.insert(0, str("$GPS INIT "+str(report.lon)+" "+str(report.lat)).encode('ascii'))
						initialized=True
						location.append([report.lon, report.lat])
					else:
						queue.insert(0, str("$GPS CURRENT "+str(report.lon)+" "+str(report.lat)).encode('ascii'))
				else:
					queue.insert(0, "$GPS GPS is not recieving data!".encode('ascii'))
	except KeyboardInterrupt:
		print("Exiting!")
		service.close()
		sys.exit()

	if not isAuto:
		while len(queue) > 0:
			time.sleep(0.2)
			service.send(queue.pop())
	else:
		queue=[]

	# ===========
	# Information
	# ===========
	os.system("clear")
	print("\nLast Command: ", lastCommand)
	print("Current Location: ", currentLocation)
	print("Next Location: ", nextLocation)
	print("Locations: ", len(location))
	print("\nMessage:", msg)
	print("Auto Mode: ", isAuto)


