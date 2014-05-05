# -*- coding: utf-8 -*-
"""
Created on Sat May  3 21:37:47 2014

@author: polchky
"""
from glove import Glove
import cv2
import numpy as np

cv2.namedWindow("window")
glove = Glove('lol',9600)
fistValues = []
openValues = []
height = 480
blackImage = np.array([[0 for f in range(640)] for f in range(height)],np.uint8)
while True:
    if len(fistValues+openValues) == 8:
        image = blackImage.copy()
        values = glove.getRawValues()
        for i in range(4):
            value = (values[i]-openValues[i]) * (height-1) / fistValues[i]
            if value > height-1:value = height-1
            if value < 0:value = 0
            image[value:,100*i+48*(i+1):(i+1)*148] = 255
    else:
        image = blackImage.copy()
        cv2.imshow("window",image)
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