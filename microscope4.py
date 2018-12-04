import cv2 as cv
import numpy as np
import time
cap = cv.VideoCapture(0)                                          # open webcam for capture

img_counter = 1
i=1

while True:
    ret, frame = cap.read()                      # Take each frame
    cv.imshow('live_feed',frame)
    k = cv.waitKey(5) & 0xFF
    if k%256 == 27:
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        while i<=10:
          img_name ="images/frame5_{}.jpg".format(img_counter)
          cv.imwrite(img_name, frame)
          print("{} written!".format(img_name))
          img_counter += 1
          i=i+1
          time.sleep(0.5)


cap.release()         # Release the webcam
cv.destroyAllWindows()# Destroy all the windows


    #time.sleep(1)

