# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 13:46:11 2014

@author: polchky
"""
import serial

class glove:
    def __init__(self, port, baud):
        self.ser = serial.Serial(port,baud)
        self.cal_low = [0,0,0]
        self.cal_high = [255,255,255]
        
    def get_values(self):
        while True:
            self.ser.write("a")
            message = self.ser.readline().rstrip()
            if message[0] == "s" and message[-1] == "e":break
        return message[1:-1].rsplit(":")
        
    def get_hand_position(self):
        values = self.get_values()
        return [1 if values(i) > (self.cal_high[i] - self.cal_low[i])/2 else 0 for i in range(3)]
        
    def calibrate(self,is_hand_closed):
        if is_hand_closed:
            self.cal_high = self.get_values()
        else:
            self.cal_low = self.get_values()