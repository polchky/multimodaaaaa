# StateMachine/Mma1/MmaTest.py
# State Machine pattern using 'if' statements
# to determine the next state.
from glove import Glove
from joystick import Joystick
from machine import State, Machine
import time
# A different subclass for each state:

class Neutral(State):
    def run(self):
        # self.key = Mma.kinect.getKey()
        #if self.key == Mma.kinect.calibrateTable:
        #    Mma.kinect.calibrateTable()
        #elif self.key == Mma.kinect.calibrateGloveOpen: 
        self.key = raw_input()
        if self.key == 'o':
            Mma.glove.calibrate(0)
       #elif self.key == Mma.kinect.calibrateGloveClosed:
        elif self.key == 'f':
            Mma.glove.calibrate(1)
    def next(self):
        #if self.key == Mma.kinect.calibrateBody:
        if self.key == 'c':
            #if Mma.kinect.isTableCalibrated():
            if Mma.glove.is_calibrated():
                return Mma.calibrating
            else:print("Glove not calibrated.")
            #else:print("Table not calibrated.")
        return Mma.neutral
    def on_start(self):
        print('entering neutral state')
        print('<o> / <f> to calibrate glove, <c> to continue\n')        

class Calibrating(State):
    def run(self):
        time.sleep(1)
        #Mma.kinect.Calibrate()
    def next(self):
        #if Mma.kinect.isCalibrationFinished():
        return Mma.waiting
        #return Mma.calibrating
    def on_stop(self):
        return
        #Mma.kinect.killDepth()
    def on_start(self):
        print('entering calibration state')
        #Mma.kinect.initCalibration()
        
        
class Waiting(State):
    def next(self):
        if Mma.glove.get_hand_position() == Mma.glove.FINGER_POSITIONS['FIST']:
            return Mma.walking
        return Mma.waiting
    def on_start(self):
        print('entering waiting state')
      
class Walking(State):
    def run(self):
        Mma.joystick.walk(Mma.glove.get_hand_position())
        return
    def next(self):
        if Mma.joystick.is_walking():
            return Mma.walking
        return Mma.playing
    def on_start(self):
        print('entering walking state')

class Playing(State):
    def run(self):
        Mma.joystick.update_buttons(Mma.glove.get_hand_position())
        #Mma.joystick.update_joystick(Mma.kinect.get_delta())
        #if Mma.joystick.is_parachute_opening():
            #Mma.kinect.check_parachute()
            
    def next(self):
        #if Mma.kinect.is_parachute_opened():
            #Mma.joystick.open_parachute()
        if Mma.joystick.is_parachute_opening():
            return Mma.neutral
        return Mma.playing
    def on_start(self):
        print('entering playing state')

class Mma(Machine):
    #init modules
    glove = Glove()
    joystick = Joystick()
    
    def __init__(self):
        # Initial state
        Machine.__init__(self, Mma.neutral)

# Static variable initialization:
Mma.neutral = Neutral()
Mma.calibrating = Calibrating()
Mma.waiting = Waiting()
Mma.playing = Playing()
Mma.walking = Walking()


Mma().run()