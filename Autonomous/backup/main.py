from matplotlib import pyplot as plt
import numpy as np
import serial
import math
import os

arduino=None
arduinoErr=''
angle=0
botCentered=False
currentSlope=0
scale=10000
Motor=None
locations = np.array([
	[80.014578, 12.145712],
	[80.014579, 12.145714],
	[80.014580, 12.145717],
	[80.014543, 12.145722],
	[80.014569, 12.145729],
	[80.014575, 12.145740]
])

nextLocation=1
locationOrigin = np.array(locations[0])
locationsTranslated = [np.array([x, y])-locationOrigin for (x, y) in locations]

scaledLocation=[[x*scale, y*scale] for (x, y) in locationsTranslated]
print(scaledLocation)
# plt.scatter([x*scale for (x, y) in locationsTranslated], [y*scale for (x, y) in locationsTranslated])
# plt.grid(True, which='both')

# plt.axhline(y=0, color='k')
# plt.axvline(x=0, color='k')
# plt.show()

def getSlope():
	currentLocationX = scaledLocation[nextLocation-1][0]
	currentLocationY = scaledLocation[nextLocation-1][1]

	slope = math.atan((scaledLocation[nextLocation][1]-currentLocationY)/(scaledLocation[nextLocation][0]-currentLocationX))
	return slope

def connectSerial():
	global arduinoErr, arduino
	try:
		arduino=serial.Serial("COM4", 115200)
		arduinoErr='None'
	except Exception as e:
		arduinoErr=str(e)
		print(e)

def centerBot(getAngle):
	global botCentered
	if(abs(angle-getAngle)>5):
		if(angle<angle):
			print("Rotate right")
		else:
			print("Rotate Left")
	else:
		botCentered=True
		
def resetAllMotors():
	for i in motorState.keys():
		motorState[i]=False
	for i in range(len(motorState)):
		Motor.digitalWrite(pinOffset+i, Motor.LOW)



connectSerial()
while True:
	# global currentSlope
	# global botCentered
	data = str(arduino.readline().rstrip()).split()
	try:
		angle=float(data[2][:-2])+180
		print(angle)
	except:
		continue

	if not botCentered:
		centerBot(0)
	else:
		if nextLocation < len(locations):
			currentSlope=getSlope()
			if abs(angle-currentSlope)>5:
				print("Recentering Bot")
				print("Current: ", currentSlope)
				centerBot(currentSlope)
			else:
				print("Move Forward!")
		
		# if bot reaches current location, move to next location
		