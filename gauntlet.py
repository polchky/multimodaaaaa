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
        position = 0
        values = self.get_values()
        for finger in range(3):
            is_closed = 1 if values(finger) > (self.cal_high[finger] - self.cal_low[finger])/2 else 0
            position += is_closed * 2**finger
        return position
        
    def calibrate(self,is_hand_closed):
        if is_hand_closed:
            self.cal_high = self.get_values()
        else:
            self.cal_low = self.get_values()