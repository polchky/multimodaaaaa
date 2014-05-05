# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 10:44:19 2014

@author: polchky
"""
import uinput, time

class Joystick:
    def __init__(self,fps):
        
        self.min_secs = 0.5 # seconds
        self.min_time = self.min_secs * fps
        print(self.min_time)
        # format: 
        #   key         'parachute'
        #   name        uinput.KEY_P
        #   value       0
        self.input_joystick ={
            'X': uinput.ABS_X,
            'Y': uinput.ABS_Y,
            'RX': uinput.ABS_RX,
            'RY': uinput.ABS_RY
        }
        self.input_termination = {
            'parachute': uinput.KEY_P,
        }
        self.input_atomic = {
            'graffiti': uinput.KEY_G,
            'fuck': uinput.KEY_F,
            'yeah': uinput.KEY_Y,
        }
        self.input_forward = {
            'forward': uinput.KEY_W,
        }
        self.key_names = dict(
            self.input_atomic.items() + 
            self.input_forward.items() +
            self.input_joystick.items() +
            self.input_termination.items()
        )
        self.names = [self.key_names[key] for key in self.key_names]
        self.keys = [str(key) for key in self.key_names]
        
        self.key_values = {}
        for key in self.keys: self.key_values[key] = [0,0,0]
        #create virtual device
        self.device = uinput.Device(tuple(self.names))
        
    def update(self,key_values):
            for key in self.keys:
                values = self.key_values[key]
                values[1] = values[0]
                values[0] = key_values[key]
                
            for key in self.input_atomic:
                values = self.key_values[key]
                if values[1]:values[2] += 1
                else:values[2] = 0
                if values[2] >= self.min_time:
                    self.emit_atomic(self.key_names[key])
                    values[2] = 0
            for key in self.input_joystick:
                values = self.key_values[key]
        
    def get_keys(self):
        return self.keys
        
        
    def emit_atomic(self,name):
        self.device.emit(name,1)
        self.device.emit(name,0)
        
        

