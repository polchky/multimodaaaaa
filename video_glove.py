# -*- coding: utf-8 -*-
"""
Created on Sat May  3 21:37:47 2014

@author: polchky
"""
from glove import Glove
import cv2, time
import numpy as np
ARDUINO_PORT = "/dev/ttyACM0"
allocated_time = 1./24

cv2.namedWindow("Glove")
glove = Glove(ARDUINO_PORT, 9600)
fistValues = []
openValues = []
height = 480
image = np.zeros((height,640))
image = np.array(image, dtype = np.uint8)
image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
capturing = False
while True:
    time_start = time.time()
    image[:,:] = 0
    if glove.is_calibrated():
        values = glove.get_calibrated_values()
        for i in range(4):
            value = values[i] * height
            color = [0,255,0] if value > height/2 else [0,0,255]
            image[value:,100*i+48*(i+1):(i+1)*148] = color
    cv2.imshow("Glove",image)
    k = cv2.waitKey(10)
    if k == ord('f'):
        glove.calibrate(1)
        fist_values = glove.cal_fist
    elif k == ord('o'):
        glove.calibrate(0)
        open_values = glove.cal_open
    elif k == ord('q'):
        cv2.destroyAllWindows()
        break
    elif k == ord('r'):
        capturing = True
        print('recording')
        writer = cv2.VideoWriter("videos/glove.avi",cv2.cv.CV_FOURCC(*"FMP4"),24,(640, 480))
    elif k == ord('s'):
        writer.release()
        print('stop recording')
        capturing = False
    if capturing:
        writer.write(image)
    time_diff = time.time()-time_start
    if time_diff < allocated_time:
        time.sleep(allocated_time-time_diff)