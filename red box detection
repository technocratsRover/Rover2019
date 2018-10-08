# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# lower and upper boundaries of the "green" in HSV
greenLower = (10, 100,100)
greenUpper = (180, 255, 255)

# initialize the list of tracked points, to draw the ball trayectory
pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, use the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])

# infinite loop
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()

	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if args.get("video") and not grabbed:
		break

	# resize the frame, blur it, and convert it to the HSV color space
	frame = imutils.resize(frame, width=600)
	output=frame.copy()
	cv2.imshow("frame",frame)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	gray = cv2.dilate(mask, None, iterations=2)
	cv2.imshow("gray",gray)
	
	#kegray = cv2.bilateralFilter( gray, 1, 10, 120 )

	#edges  = cv2.Canny( gray, 10, CANNY )

	#kernel = cv2.getStructuringElement( cv2.MORPH_RECT, ( MORPH, MORPH ) )

	#closed = cv2.morphologyEx( edges, cv2.MORPH_CLOSE, kernel )

	_,contours, h = cv2.findContours( gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )
	approx=[]	
	for cont in contours:
		if cv2.contourArea(cont)>5000:
			arc_len=cv2.arcLength(cont, True)
			approx=cv2.approxPolyDP(cont,0.15*arc_len,True)
		print(len(approx))
		if(len(approx)==4):
			print("rectangle")	

	key = cv2.waitKey(1) & 0xFF
        
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
