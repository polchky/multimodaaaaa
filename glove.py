# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 13:46:11 2014

@author: polchky
"""
import serial

class Glove:
    def __init__(self, port, baud):
        self.ser = serial.Serial(port,baud)
        self.calFist = []
        self.calOpen = []
        
    def getRawValues(self):
        while True:
            self.ser.write("a")
            message = self.ser.readline().rstrip()
            if message[0] == "s" and message[-1] == "e":break
        return message[1:-1].rsplit(":")
        
    def isCalibrated(self):
        return len(self.calFist + self.calOpen) == 8
        
    def getHandPosition(self):
        values = self.getRawValues()
        return [1 if values(i) > (self.calFIst[i] - self.calOpen[i])/2 else 0 for i in range(3)]
        
    def calibrate(self,isHandClosed):
        if isHandClosed:
            self.calFist = self.getRawValues()
        else:
            self.calOpen = self.getRawValues()
            
Glove.fuck = [0,0,1,0]
Glove.yeah = [0,1,1,0]
Glove.fist = [0,0,0,0]
Glove.open = [1,1,1,1]
Glove.point = [0,1,0,0]