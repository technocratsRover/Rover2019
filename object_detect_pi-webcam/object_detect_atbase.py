# Import socket module 
# this is for both the analysis of picam_sent_frame and webcam_sent_frame
import socket
import numpy as np
import cv2 as cv
import time

openingKernel = cv.getStructuringElement(cv.MORPH_RECT, (10, 10)) # Make a kernel for closing (noise removal)
openingKernelRed = cv.getStructuringElement(cv.MORPH_RECT, (2, 2))

# Limits for green range
lower_green = np.array([37, 80, 40])
upper_green = np.array([95, 255, 255])

# Limits for blue range
lower_blue = np.array([110, 50, 50])
upper_blue = np.array([130, 255, 255])

# Limits for yellow range
lower_yellow = np.array([20, 80, 40])
upper_yellow = np.array([35, 255, 255])

# Limits for red
lower_red = np.array([170, 80, 40])
upper_red = np.array([180, 255, 255])
# Create a socket object 
s = socket.socket()          
  
# Define the port on which you want to connect 
PORT = 8002              
  
# connect to the server on local computer 
s.connect(('192.168.1.13', PORT)) 
  
# receive data from the server

while True:
    data = s.recv(921600)
    # buffer is 921600 since 640x480x3 values.
    image = np.frombuffer(data, dtype = np.uint8)
    print(image)
    print(image.shape)
    #print(data)
    print(image[0:3])
    newImg = image.reshape((480,640,3))
    print(newImg)

    hsv = cv.cvtColor(newImg, cv.COLOR_BGR2HSV) # Take each newImg

    # Threshold the HSV image to get only desired colors
    maskGreen = cv.inRange(hsv, lower_green, upper_green)
    maskBlue = cv.inRange(hsv, lower_blue, upper_blue)
    maskYellow = cv.inRange(hsv, lower_yellow, upper_yellow)
    #maskRed = cv.inRange(hsv, lower_red, upper_red)


    # # Clear noise from mask by opening it, then apply gaussian blur
    maskGreen = cv.morphologyEx(maskGreen, cv.MORPH_OPEN, openingKernel)
    maskGreen = cv.GaussianBlur(maskGreen, (5, 5), 0)

    maskBlue = cv.morphologyEx(maskBlue, cv.MORPH_OPEN, openingKernel)
    maskBlue = cv.GaussianBlur(maskBlue, (5, 5), 0)

    maskYellow = cv.morphologyEx(maskYellow, cv.MORPH_OPEN, openingKernel)
    maskYellow = cv.GaussianBlur(maskYellow, (5, 5), 0)

    #maskRed = cv.morphologyEx(maskRed, cv.MORPH_OPEN, openingKernelRed)
    #maskRed = cv.GaussianBlur(maskRed, (5, 5), 0)

    # Using threshold incase the image is not binary, can be removed
    _, threshGreen = cv.threshold(maskGreen, 100, 255, cv.THRESH_BINARY)
    _, threshBlue = cv.threshold(maskBlue, 100, 255, cv.THRESH_BINARY)
    _, threshYellow = cv.threshold(maskYellow, 100, 255, cv.THRESH_BINARY)
    #_, threshRed = cv.threshold(maskRed, 100, 255, cv.THRESH_BINARY)

    _,contoursGreen, _ = cv.findContours(threshGreen, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    _,contoursBlue, _ = cv.findContours(threshBlue, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    _,contoursYellow, _ = cv.findContours(threshYellow, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
  #_,contoursRed, _ = cv.findContours(threshRed, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

  # Bitwise-AND mask and original image
    mask = cv.bitwise_or(maskBlue, maskGreen)
    mask = cv.bitwise_or(mask, maskYellow)
  #mask = cv.bitwise_or(mask, maskRed)
    res = cv.bitwise_and(newImg, newImg, mask=mask)

    numGreen = len(contoursGreen)
  #numRed=len(contoursRed)
    numBlue=len(contoursBlue)
    numYellow=len(contoursYellow)
    t = ':True'
    f = ':False'
    if(numBlue>5):
      bottle = t
    else:
      bottle = f
    mask = cv.inRange(hsv, lower_red, upper_red)
    mask = cv.erode(mask,None, iterations = 2)
    gray = cv.dilate(mask,None, iterations = 2)
    _,contoursRed, h = cv.findContours(gray, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    approx = []
    box = f
    for cont in contoursRed:
      if cv.contourArea(cont)>500:
        arc_len = cv.arcLength(cont,True)
        approx = cv.approxPolyDP(cont, 0.15*arc_len, True)
    #print(len(approx))
      if (len(approx)==4):
        box = t
  #if(numRed>100):
  #  box = t
  #else:
  #  box = f
    if(numGreen>4):
      ball = t
    else:
      ball = f
    if(numYellow>2):
      disc = t
    else:
      disc = f
    result = "Bottle"+bottle+"\nBox"+box+"\nBall"+ball+"\nDisc"+disc+"\n"
    print(result)
    # this gives the RGB value of the first pixel
    #https://stackoverflow.com/questions/33622617/reshape-1d-numpy-array-to-3d-with-x-y-z-ordering
    # similarly access 3 value at a time and store as single element in numpy array of 
    # 480x640 size (480 rows since image height i.e top to bottom will be 480)
    # (similarly 640 rows since image width i.e left to right will be 640)
    # break statement is only to test for one capture 
    # remove break for contionuous execution 
    time.sleep(1)
    #break
    #convert the resultant string back to numpy array and use for opencv
# close the connection 
s.close()   
