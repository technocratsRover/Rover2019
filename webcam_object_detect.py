import cv2 as cv
import numpy as np
import os
import time
import socket         

s = socket.socket()        
port = 9000
s.bind(('', port))		 
s.listen(5)
c, addr = s.accept() #sendind objects status to base

cap = cv.VideoCapture(0)                                          # open webcam for capture
openingKernel = cv.getStructuringElement(cv.MORPH_RECT, (10, 10)) # Make a kernel for closing (noise removal)
openingKernelRed = cv.getStructuringElement(cv.MORPH_RECT, (2, 2))

# define range of blue color in HSV
# Range for green in HSV
# lower = 40 40 40
# upper = 80 255 255
# TODO: Tweek these values to detect all ranges of color properly

# Values calculated from: https://alloyui.com/examples/color-picker/hsv
# Limits for green range
lower_green = np.array([37, 80, 40])
upper_green = np.array([95, 255, 255])

# Limits for blue range
lower_blue = np.array([100, 80, 50])
upper_blue = np.array([125, 255, 255])

# Limits for yellow range
lower_yellow = np.array([20, 80, 40])
upper_yellow = np.array([35, 255, 255])

# Limits for red
lower_red = np.array([170, 80, 40])
upper_red = np.array([180, 255, 255])

while True:
  os.system('clear')
  _, frame = cap.read()                      # Take each frame
  hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV) # Take each frame

  # Threshold the HSV image to get only desired colors
  maskGreen = cv.inRange(hsv, lower_green, upper_green)
  maskBlue = cv.inRange(hsv, lower_blue, upper_blue)
  maskYellow = cv.inRange(hsv, lower_yellow, upper_yellow)
  maskRed = cv.inRange(hsv, lower_red, upper_red)


  # # Clear noise from mask by opening it, then apply gaussian blur
  maskGreen = cv.morphologyEx(maskGreen, cv.MORPH_OPEN, openingKernel)
  maskGreen = cv.GaussianBlur(maskGreen, (5, 5), 0)

  maskBlue = cv.morphologyEx(maskBlue, cv.MORPH_OPEN, openingKernel)
  maskBlue = cv.GaussianBlur(maskBlue, (5, 5), 0)

  maskYellow = cv.morphologyEx(maskYellow, cv.MORPH_OPEN, openingKernel)
  maskYellow = cv.GaussianBlur(maskYellow, (5, 5), 0)

  maskRed = cv.morphologyEx(maskRed, cv.MORPH_OPEN, openingKernelRed)
  maskRed = cv.GaussianBlur(maskRed, (5, 5), 0)

  # Using threshold incase the image is not binary, can be removed
  _, threshGreen = cv.threshold(maskGreen, 100, 255, cv.THRESH_BINARY)
  _, threshBlue = cv.threshold(maskBlue, 100, 255, cv.THRESH_BINARY)
  _, threshYellow = cv.threshold(maskYellow, 100, 255, cv.THRESH_BINARY)
  _, threshRed = cv.threshold(maskRed, 100, 255, cv.THRESH_BINARY)

  _,contoursGreen, _ = cv.findContours(threshGreen, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
  _,contoursBlue, _ = cv.findContours(threshBlue, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
  _,contoursYellow, _ = cv.findContours(threshYellow, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
  _,contoursRed, _ = cv.findContours(threshRed, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

  # Bitwise-AND mask and original image
  mask = cv.bitwise_or(maskBlue, maskGreen)
  mask = cv.bitwise_or(mask, maskYellow)
  mask=cv.bitwise_or(mask, maskRed)
  res = cv.bitwise_and(frame, frame, mask=mask)

  numGreen = len(contoursGreen)
  numRed=len(contoursRed)
  numBlue=len(contoursBlue)
  numYellow=len(contoursYellow)
  t = ':True'
  f = ':False'
  if(numBlue>5):
    bottle = t
  else:
    bottle = f
  if(numRed>100):
    box = t
  else:
    box = f
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
  c.send(result.encode())
  time.sleep(2)
  
  # for c in contoursGreen:
  #   # To avoid false-positives, the green object should be sufficiently big
  #   if cv.contourArea(c) > 700:
  #     # Calculate center of mass to put the text
  #     M = cv.moments(c)
  #     cX = int(M["m10"] / M["m00"])
  #     cY = int(M["m01"] / M["m00"])

  #     cv.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
  #     cv.putText(frame, "green ball", (cX - 10, cY - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
  #     cv.drawContours(res, [c], -1, (255, 0, 255), 3)

  # for c in contoursBlue:
  #   # To avoid false-positives, the green object should be sufficiently big
  #   if cv.contourArea(c) > 1000:
  #     # Calculate center of mass to put the text
  #     M = cv.moments(c)
  #     cX = int(M["m10"] / M["m00"])
  #     cY = int(M["m01"] / M["m00"])

  #     cv.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
  #     cv.putText(frame, "bottle", (cX - 10, cY - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
  #     cv.drawContours(res, [c], -1, (255, 0, 255), 3)

  # for c in contoursYellow:
  #   # To avoid false-positives, the green object should be sufficiently big
  #   if cv.contourArea(c) > 1000:
  #     # Calculate center of mass to put the text
  #     M = cv.moments(c)
  #     cX = int(M["m10"] / M["m00"])
  #     cY = int(M["m01"] / M["m00"])

  #     cv.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
  #     cv.putText(frame, "yellow disk", (cX - 10, cY - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
  #     cv.drawContours(res, [c], -1, (255, 0, 255), 3)

  # for c in contoursRed:
  # # To avoid false-positives, the green object should be sufficiently big
  #   if cv.contourArea(c) > 1000:
  #     # Calculate center of mass to put the text
  #     M = cv.moments(c)
  #     cX = int(M["m10"] / M["m00"])
  #     cY = int(M["m01"] / M["m00"])

  #     cv.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
  #     cv.putText(frame, "red box", (cX - 10, cY - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
  #     cv.drawContours(res, [c], -1, (255, 0, 255), 3)
  # # Show the image and the result
  # cv.imshow('res', res)
  # cv.imshow('blue', maskBlue)
  # cv.imshow('green', maskGreen)
  # cv.imshow('yellow', maskYellow)
  # cv.imshow('red', maskRed)
  # cv.imshow('res', res)
  # EXIT if 'esc' key is pressed
  k = cv.waitKey(5) & 0xFF
  if k == 27:
    break

cap.release()         # Release the webcam
cv.destroyAllWindows()# Destroy all the windows
c.close() # close socket after use
