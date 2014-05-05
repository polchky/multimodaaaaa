# -*- coding: utf-8 -*-
"""
Created on Sat May  3 21:37:47 2014

@author: polchky
"""
from glove import Glove
import cv2
import numpy as np
ARDUINO_PORT = "/dev/ttyACM0"

cv2.namedWindow("Glove")
glove = Glove(ARDUINO_PORT, 9600)
fistValues = []
openValues = []
height = 480
image = np.zeros((height,640))

while True:
    image[:,:] = 0
    if glove.isCalibrated():
        values = glove.getCalibratedValues()
        for i in range(4):
            value = values[i] * height
            image[value:,100*i+48*(i+1):(i+1)*148] = 255
    cv2.imshow("Glove",image)
    k = cv2.waitKey(10)
    if k == ord('f'):
        glove.calibrate(1)
        fistValues = glove.calFist
    elif k == ord('o'):
        glove.calibrate(0)
        openValues = glove.calOpen
    elif k == ord('q'):
        cv2.destroyAllWindows()
        break