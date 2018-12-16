# TODO:
# 1. Figure out a way to check if gps is not connected

# ALGO:
# 1. Center the bot at north - Not needed anymore
# 2. Get the next Location slope
# 3. Rotate the bot that much angle
# 4. While the bot has not reached the location, move forward
# 5. If the bot is out of the slope angle, recenter it


# =======
# Imports
# =======
import numpy as np
import math
import os
from compass import Compass
from motor import Motor
from roverGps import RoverGps
from time import sleep
from math import pi as PI


# =========
# Variables
# =========
nextLocationIndex=0
roverMotor=None			# Doesnt fucking work
compass=None
roverGps=None



# ======================
# Set locations to go to
# ======================

locations=[
	[12.842517, 80.156030],
	[12.842613, 80.156073],
	[12.842803, 80.156168],
	[12.842883, 80.156212]
]


# ================
# Helper Functions
# ================

# Returns the angle to move the rover to
def getSlope(currentLocation):
	global nextLocationIndex
	global scaledLocations
	global locations
	x1 = currentLocation[0]
	y1 = currentLocation[1]
	
	x2 = locations[nextLocationIndex][0]
	y2 = locations[nextLocationIndex][1]
	# print(locations[nextLocationIndex], end=" ")

	try:
		slope = 90-math.atan((x2-x1)/(y2-y1))*180/PI
		if((x2-x1)<0):
			slope=slope-180
	except ZeroDivisionError:
		print("\n\nDivide by 0")
		return

	return slope

# Function to move bot left or right according to the slope
# It returns true if rover is centered and false if rover is not centered
def centerBot(compass, getAngle, roverGps, roverMotor, threshold=0):
	
	currentLocation = roverGps.getGpsData()
	getAngle = getSlope(currentLocation)

	try:
		angle = compass.getCompassAngle()
	except ValueError as e:
		print("\nError: Inside centerBot: Calibrate Compass")
		return False
	try:
		if abs(abs(angle)-abs(getAngle))>threshold or np.sign(angle)!=np.sign(getAngle):
			print("Centering Rover!",currentLocation, locations[nextLocationIndex], end=": ")
			if(angle>getAngle):
				print("Rotate left ", getAngle, angle)
				# roverMotor.moveMotor('right')
			else:
				print("Rotate right ", getAngle, angle)
				# roverMotor.moveMotor('left')
			return False
		else:
			return True
	except TypeError:
		return False
	










# =============
# Main Function
# =============
def main():
	# Local functions in main function
	global nextLocationIndex
	global locations
	global roverMotor
	botCentered = False
	locationAccuracy=0.00001

	print("Setting devices...")
	compass = Compass("/dev/ttyACM0")
	# roverMotor = Motor("/dev/ttyACM2")
	roverGps = RoverGps()
	# roverMotor.resetAllMotors()
	print("All device set!")
	sleep(2)

	# Set the bot to point at next location
	while not botCentered:
		if centerBot(compass, 0, roverGps, roverMotor, 10):
			botCentered=True
		# sleep(0.1)
		# os.system("clear")
	# botCentered=False
	# roverMotor.moveMotor("stop")
	os.system("clear")
	print("Rover centered!")
	# roverMotor.resetAllMotors()
	sleep(2)
	
	print("Locations:", locations)
	input('Press anything to continue!')
	
	# =========
	# Main Loop
	# =========
	while nextLocationIndex < len(locations):
		# roverMotor.resetAllMotors()
		try:
			currentLocation = roverGps.getGpsData()
			# print(roverGps)
		except ValueError:
			print("GPS not set")
			continue
		if currentLocation[0]==None:
			print("GPS no location")
			continue
			
		if abs(currentLocation[0]-locations[nextLocationIndex][0])<locationAccuracy and  abs(currentLocation[1]-locations[nextLocationIndex][1])<locationAccuracy:
			# roverMotor.moveMotor("stop")
			nextLocationIndex+=1
			if nextLocationIndex>=len(locations):
				break
			print(locations)
			print("Location Reached!", currentLocation)
			print("Press any key to continue")
			input()
			# sleep(2)
			# Center bot to north
			botCentered=False
			while not botCentered:
				# os.system("clear")
				
				if centerBot(compass, 0, roverGps, roverMotor, 20):
					print()
					botCentered=True
			botCentered=False
			print("Press anything to continue to location", locations[nextLocationIndex])
			input()
			continue
		
		slope = getSlope(currentLocation)
		# Move the rover to this slope    
		while not botCentered:
			# os.system("clear")
			slope = getSlope(currentLocation)
			
			if centerBot(compass, slope, roverGps, roverMotor, 15):
				botCentered=True
			# sleep(0.5)
		if not centerBot(compass, slope, roverGps, roverMotor, 15):
			print()
			botCentered=False

		# # Move bot forward
		# # os.system("clear")
		try:
			print("Move Forward", roverGps.getGpsData(), locations[nextLocationIndex] ,slope, compass.getCompassAngle())
			# roverMotor.moveMotor('forward')
		except ValueError:
			print("Compass Value error")
	print("Finished!")

if __name__=="__main__":
	main()

