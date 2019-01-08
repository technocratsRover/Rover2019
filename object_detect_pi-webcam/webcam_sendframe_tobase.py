#import picamera
import numpy as np
import socket
import time
import cv2 as cv

PORT = 8002

s = socket.socket()
s.bind(('',PORT))
s.listen(5)

c,addr = s.accept()

#with picamera.PiCamera() as camera:
#    camera.resolution = (640,480)
 #   camera.framerate = 24
 #   time.sleep(2) # give warmup time
 #   obj = np.empty((480,640,3), dtype = np.uint8)
 #   while True:
 #       camera.capture(obj,'rgb')
 #       print(obj)
 #       c.send(str(obj).encode('ascii'))

camera = cv.VideoCapture(0)
while True:
    ret,frame = camera.read()
    #don't remove ret, otherwise socket will also send TRUE/FALSE along with frame array
    #print(type(frame))
    print(frame)
    #print(len(frame))
    #c.send(str(frame).encode('ascii'))
    #convrt to bytes and send via socket to base
    frame = frame.tobytes()
    c.send(frame)
    time.sleep(1)
    #break
    # break statement is to only test for one frame, for complete video remove it
