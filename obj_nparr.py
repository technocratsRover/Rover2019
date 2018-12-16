import picamera
import numpy as np
import socket
import time

PORT = 8001

s = socket.socket()
s.bind(('',PORT))
s.listen(5)

c,addr = s.accept()

with picamera.PiCamera() as camera:
    camera.resolution = (640,480)
    camera.framerate = 24
    time.sleep(2) # give warmup time
    obj = np.empty((480,640,3), dtype = np.uint8)
    while True:
        camera.capture(obj,'rgb')
        print(obj)
        c.send(str(obj).encode('ascii'))
