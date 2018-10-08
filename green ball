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
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

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
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	gray = cv2.dilate(mask, None, iterations=2)
	cv2.imshow("gray",gray)
	circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=10, maxRadius=100)
	print circles
	
	# ensure at least some circles were found
	if circles is not None:
		print("FOUND")
		# convert the (x, y) coordinates and radius of the circles to integers
		circles = np.round(circles[0, :]).astype("int")
		
		# loop over the (x, y) coordinates and radius of the circles
		for (x, y, r) in circles:
			# draw the circle in the output image, then draw a rectangle in the image
			# corresponding to the center of the circle
			cv2.circle(output, (x, y), r, (0, 255, 0), 4)
			cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
			#time.sleep(0.5)
			print "Column Number: "
			print x
			print "Row Number: "
			print y
			print "Radius is: "
			print r
	else:
		print("not found")
	# Display the resulting frame
	cv2.imshow('gray',gray)
	cv2.imshow('frame',output)

	# show the frame to our screen
	#cv2.imshow("Frame", frame)
	# cv2.imshow("Frame", mask)
	key = cv2.waitKey(1) & 0xFF
        
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
