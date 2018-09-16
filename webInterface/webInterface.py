import gps
import serial
from flask import Flask, render_template, request, jsonify
# import threading


app = Flask(__name__)
arduino=serial.Serial("/dev/ttyACM0", 9600)
response = dict()

# ==========
# GPS Socket
# ==========
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

# =========
# Variables
# =========
isAuto = False
initialized = False
queue = []
location=[]
gpsStarted = False

currentLocation=dict({})
nextLocation='NoR'
textPastCommand='NoR'
err='None'
gpsErr='None'

@app.route("/")
def sendData():
	return render_template("home.html")


@app.route("/getData", methods=['GET'])
def gpsData():
	global initialized
	report = session.next()
	print(report)
	response['report']=dict({'dat':"YES"})
	if report['class']=='TPV':
		gpsStarted=True
		gpsErr='None'
		if hasattr(report, 'time') and hasattr(report, 'lon') and hasattr(report, 'lat'):
				currentLocation['lon']=report.lon
				currentLocation['lat']=report.lat
				if not initialized:		
					initialized=True
					location.append([report.lon, report.lat])
	else:
		currentLocation['lat']='Nor'
		currentLocation['lon']='Nor'
		if not gpsStarted:
			gpsErr='GPS has not initialized! Check connectivity'

	response['textPastCommand']=textPastCommand
	response['gpsError']=gpsErr
	response['currentLocationLat']=currentLocation['lat']
	response['currentLocationLon']=currentLocation['lon']
	response['nextLocation']=nextLocation
	return jsonify(**response)

@app.route("/getSensor", methods=['GET', 'POST'])
def returnSensorData():
	data=arduino.readline()
	data = data.decode('utf-8').rstrip()
	data=data.split(' ')
	ph, temp, moisture = data
	return jsonify(sensorDataPH=ph, sensorDataTemp=temp, sensorDataMoisture=moisture)

app.debug=True
app.run('192.168.43.30', debug=True)
