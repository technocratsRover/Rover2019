import gps
import serial
from flask import Flask, render_template, request, jsonify
# import threading

# =========
# Variables
# =========
isAuto = False
initialized = False
locationsPassed=[]
location=[]
gpsStarted = False
initializedNext=False
currentLocation=dict({'lat': 'None', 'lon':'None'})
nextLocation=dict({'lat': 'None', 'lon':'None'})
nextLocationIndex=1
textPastCommand='NoR'
err='None'
gpsErr='None'
arduinoErr='None'
response = dict()
arduino=None
session=None
app = Flask(__name__)

def connectSerial():
	global arduinoErr, arduino
	try:
		arduino=serial.Serial("/dev/ttyACM0", 9600)
		arduinoErr='None'
	except Exception as e:
		arduinoErr=str(e)
		response['serialError']=arduinoErr


# ==========
# GPS Socket
# ==========
def connectGPS():
	global gpsErr
	try:
		session = gps.gps("localhost", "2947")
		session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
		gpsErr='None'
	except Exception as e:
		gpsErr=str(e)
		response['gpsError']=gpsErr

# Initial Connection
connectGPS()
connectSerial()

@app.route("/")
def sendData():
	return render_template("home.html")

@app.route("/frameDivide")
def sendFrame():
	return render_template("frameDivide.html")

@app.route("/getGps", methods=['GET'])
def gpsData():
	global initialized, gpsErr, session, nextLocationIndex
	if gpsErr=='None':
		report = session.next()
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
					if abs(currentLocation['lon']-nextLocation['lat'])<2 and len(location)>2:
						locationsPassed.append(nextLocationIndex)
						nextLocationIndex+=1
						nextLocation['lat']=location[nextLocationIndex][0]
						nextLocation['lat']=location[nextLocationIndex][1]
		else:
			currentLocation['lat']='Nor'
			currentLocation['lon']='Nor'
			if not gpsStarted:
				gpsErr='GPS has not initialized! Check connectivity'
	else:
		report=dict({})

	return jsonify(
		currentLocationLat=currentLocation['lat'],
		currentLocationLon=currentLocation['lon'],
		locationListBody=location,
		report=report,
		gpsError=gpsErr
		)
	
@app.route("/getSensor", methods=['GET', 'POST'])
def returnSensorData():
	ph='NoR'
	temp='NoR'
	moisture='NoR'
	if arduinoErr=='None':
		data=arduino.readline()
		data = data.decode('utf-8').rstrip()
		data=data.split(' ')
		ph, temp, moisture = data
	return jsonify(sensorDataPH=ph, sensorDataTemp=temp, sensorDataMoisture=moisture, serialError=arduinoErr)

@app.route("/executeCommand", methods=["POST"])
def executeCommand():
	global location, commandError, initializedNext
	command=request.json['command'].split(' ')
	print(command)
	operation = command[0]
	values=None
	if operation in ["ADD"]:
		values = command[1:]
	
	if operation=='ADD':
		if not (values in location):
			location.append(values)
			commandError='None'
			if initializedNext==False and len(location)>2:
				nextLocation['lat']=location[nextLocationIndex][0]
				nextLocation['lat']=location[nextLocationIndex][1]
				initializedNext=True
		else:
			commandError='Location already exists!'
	elif operation=="CLEAR":
		location=[]
		commandError="None"
	else:
		commandError = 'Unknown Command!'
	
	return jsonify(locationListBody=location, commandError=commandError)

@app.route("/reset/<service>", methods=['GET'])
def reset(service):
	global commandError
	if service=='gps':
		print("Reset GPS")
		connectGPS()
	elif service=='serial':
		print("Reset Serial")
		connectSerial()
	elif service=='command':
		commandError='None'
	else:
		pass
	return jsonify(value='False', commandError=commandError)
		
@app.route("/delLocation/<index>")
def deleteLocation(index):
	index=int(index)
	global location
	del location[index]
	return jsonify(locationListBody=location)

app.debug=True
app.run('', debug=True,port=8000)
