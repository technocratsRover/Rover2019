import cv2
import numpy as np

img = cv2.imread('C:\\Users\\nckdj\\Desktop\\VIT Workship\\Technocrats\\Soil.jpg')
hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
lower_brown = np.array([10,100,20])
upper_brown = np.array([20,255,200])
mask = cv2.inRange(hsv,lower_brown,upper_brown)
res = cv2.bitwise_and(img,img,mask=mask)
cv2.imshow('image',img)
cv2.imshow('mask',mask)
cv2.imshow('res',res)
k = cv2.waitKey(0)
cv2.destroyAllWindows()
"""
[10, 100, 20] to [20, 255, 200] in HSV:

[[[120 190 165]]]"""
