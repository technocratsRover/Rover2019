from flask import Flask, render_template, request, jsonify
import serial
from motor import Motor
app = Flask(__name__)

# ================
# Global Variables
# ================
motorPath = "/dev/ttyACM0"
motorConnected=False

# ================
# Connecting Motor
# ================
try:
	roverMotor = Motor(motorPath)
	motorConnected=True
except serial.serialutil.SerialException:
	motorConnected = False

# ================
# Helper Functions
# ================
def resetMotor(roverMotor):
	global motorConnected
	try:
		roverMotor.connectMotor(motorPath)
		motorConnected=True
	except serial.serialutil.SerialException:
		motorConnected = False

# ======
# Routes
# ======
@app.route('/')
def renderHome():
	return render_template('index.html')
		
@app.route("/setMotors", methods=["GET"])
def runMotors():
	global roverMotor
	if not motorConnected:
		return "Error: Motor not connected!"
	try:
		if request.args.get('reset'):
			resetMotor(roverMotor)
			return "Reset!"
		if request.args['front']=='true':
			roverMotor.moveMotor('forward')
			return "Forward"
		elif request.args['right']=='true':
			roverMotor.moveMotor('right')
			return "Right"
		elif request.args['back']=='true':
			roverMotor.moveMotor('back')
			return "Backward"
		elif request.args['left']=='true':
			roverMotor.moveMotor('left')
			return "Left"
		elif request.args['stop']=='true':
			roverMotor.moveMotor('stop')
			return "Stopped!"
		else:
			return "Error: Unknown Command!"
	except KeyError:
		roverMotor.moveMotor('stop')
		return "Error: Unknown Key!"
	
@app.route("/setRPM/<int:value>", methods=["GET"])
def setRPM(value):
	global roverMotor
	if value>255:
		return "Error: Invalid value range!"
	
	roverMotor.setRPM(value)
	return "Success!"


# ===================
# Running application
# ===================
app.debug = True
app.run('',port=5000, debug=True)