# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 13:46:11 2014

@author: polchky
"""
import serial

class Glove:
    FINGER_COUNT = 4
    FINGER_POSITIONS = {
        'FUCK':  [False, False, True, False],
        'YEAH': [[False, True, True, False],
                 [True, False, False, False]],
        'FIST':  [False, False, False, False],
        'OPEN':  [True, True, True, True],
        'GRAF':  [False, True, False, False]
    }
    
    def __init__(self, port = "/dev/ttyACM0", baud=9600):
        self.ser = serial.Serial(port,baud)
        self.cal_fist = []
        self.cal_open = []
        
    def is_calibrated(self):
        return len(self.cal_fist + self.cal_open) == 2 * Glove.FINGER_COUNT
        
    def get_raw_values(self):
        while True:
            self.ser.write("a")
            message = self.ser.readline().rstrip()
            if message[0] == "s" and message[-1] == "e":break
        return [int(v) for v in message[1:-1].rsplit(":")[:-1]]

    def get_calibrated_values(self):
        values = self.get_raw_values()
        cal = []
        for i in range(Glove.FINGER_COUNT):
            value = float(values[i]-self.cal_open[i]) / (self.cal_fist[i] - self.cal_open[i])
            if value < 0:value = 0
            if value > 1: value = 1
            cal.append(value)
        return cal
        
    def get_hand_position(self):
        values = self.get_calibrated_values()
        return [values[i] < 0.5 for i in range(Glove.FINGER_COUNT)]
     
    def calibrate(self,is_hand_closed):
        if is_hand_closed:
            self.cal_fist = self.get_raw_values()
        else:
            self.cal_open = self.get_raw_values()
  