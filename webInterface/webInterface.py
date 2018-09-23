import gps
import serial
import nanpy
import collections
from nanpy import ArduinoApi, SerialManager
from flask import Flask, render_template, request, jsonify
# import threading

# =========
# Variables
# =========
# Boolean Variables / Flags
isAuto = False
initialized = False
gpsStarted = False
initializedNext=False
# Object initializations
arduino=None
session=None
Motor = None
# Variables Regarding locations
locationsPassed=[]
location=[]
currentLocation=dict({'lat': 'None', 'lon':'None'})
nextLocation=dict({'lat': 'None', 'lon':'None'})
nextLocationIndex=1
# Variables regarding error
# textPastCommand='NoR' # !Remove this
err='None'
gpsErr='None'
arduinoErr='None'
# Dictionary to store response
response = dict()

# ===============
# Motor Variables
# ===============
# FRONT BACK RIGHT LEFT
motorState = collections.OrderedDict({
	'front': False, 
	'back': False, 
	'left': False,
	'right': False
})
# The motors pins are pinOffset + 0, pinOffset + 1, pinOffset + 2, pinOffset + 3
pinOffset = 7

def resetAllMotors():
	for i in motorState.keys():
		motorState[i]=False
	for i in range(len(motorState)):
		Motor.digitalWrite(pinOffset+i, Motor.LOW)


# Set up flask
app = Flask(__name__)

# ====================
# Connecting Functions
# ====================
def connectSerial():
	global arduinoErr, arduino
	try:
		arduino=serial.Serial("/dev/ttyUSB0", 9600)
		arduinoErr='None'
	except Exception as e:
		arduinoErr=str(e)
		response['serialError']=arduinoErr

def connectGPS():
	global gpsErr
	try:
		# GPS Socket
		session = gps.gps("localhost", "2947")
		session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
		gpsErr='None'
	except Exception as e:
		gpsErr=str(e)
		response['gpsError']=gpsErr

def connectMotor():
	global Motor
	try:
		connection = SerialManager("/dev/ttyACM0") #CHANGE THIS
		Motor = ArduinoApi(connection=connection)
	except Exception as e:
		print("Failed to connect to arduino!", e)


# def motor():
# 	print("Motor thread Started!")
# 	while True:
# 		for i in range(len(motorState)):
# 			if motorState[i]:
# 				a.digitalWrite(pinOffset+i, a.HIGH)
# 			else:
# 				a.digitalWrite(pinOffset+i, a.LOW)

# Initial Connection
connectGPS()
connectSerial()
connectMotor()
# Motor.digitalWrite(7, Motor.HIGH)
# ======
# Routes
# ======
@app.route("/")																			# Home page
def sendData():
	return render_template("home.html")

@app.route("/frameDivide")													# Cam Page
def sendFrame():
	return render_template("frameDivide.html")

@app.route("/getGps", methods=['GET'])							# Ajax route to send GPS Data when requested
def gpsData():
	global initialized, gpsErr, session, nextLocationIndex
	if gpsErr=='None':
		report = session.next()
		response['report']=dict({'dat':"YES"})	#! Remove this, this is only to check
		if report['class']=='TPV':
			gpsStarted=True
			gpsErr='None'
			if hasattr(report, 'time') and hasattr(report, 'lon') and hasattr(report, 'lat'):
					currentLocation['lon']=report.lon
					currentLocation['lat']=report.lat
					if not initialized:	#? Forgot what it does
						initialized=True
						location.append([report.lon, report.lat])
					# If the gps coordinate is at the next location, set the next location to next location
					#! A try catch is required here
					if abs(currentLocation['lon']-nextLocation['lat'])<2 and len(location)>2:
						locationsPassed.append(nextLocationIndex)
						nextLocationIndex+=1
						nextLocation['lat']=location[nextLocationIndex][0]
						nextLocation['lat']=location[nextLocationIndex][1]
		else:
			# GPS is not getting data
			currentLocation['lat']='Nor'
			currentLocation['lon']='Nor'
			if not gpsStarted:
				gpsErr='GPS has not initialized! Check connectivity'
	else:
		report=dict({})

	#! Add nextLocation lat and lon as well
	return jsonify(
		currentLocationLat=currentLocation['lat'],
		currentLocationLon=currentLocation['lon'],
		locationListBody=location,
		report=report,
		gpsError=gpsErr
		)
	
@app.route("/getSensor", methods=['GET', 'POST'])		# Ajax route to send sensor data #! Remove POST Method?
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

@app.route("/executeCommand", methods=["POST"])			# Ajax route to execute commands
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

@app.route("/reset/<service>", methods=['GET'])			# Ajax route to reset errors and devices
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
		
@app.route("/setMotors", methods=["GET"])
def runMotors():
	err='None'
	# resetAllMotors()
	try:
		resetAllMotors()
		print(request.args)
		if request.args.get('reset'):
			resetAllMotors()
			return jsonify(err="Motor Reset")
		
		for i in request.args:
			if request.args.get(i)=='true':
				motorState[i]=True
				print(motorState)
				pin = pinOffset + int(list(motorState.keys()).index(i))
				print("Pin: ", pin)
				Motor.digitalWrite(pin, Motor.HIGH)
		return jsonify(motorState)
	except keyError:
		print("RESET")
		resetAllMotors()
		return jsonify(err="Invalid motor Number, Valid options: [0, 1, 2, 3, 4]")

@app.route("/delLocation/<index>")									# Ajax method to delete datas
def deleteLocation(index):
	index=int(index)
	global location
	del location[index]
	return jsonify(locationListBody=location)


# Run the app
app.debug=True
app.run('', debug=True,port=8000)
