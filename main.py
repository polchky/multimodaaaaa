# StateMachine/Mma1/MmaTest.py
# State Machine pattern using 'if' statements
# to determine the next state.
import time
from kinect import Kinect
from glove import Glove
from joystick import Joystick
from machine import State, Machine
from manager import Manager
# A different subclass for each state:

class Neutral(State):
    def run(self):
        self.key = Mma.kinect.getKey()
        if self.key == Mma.kinect.calibrateTable:
            Mma.kinect.calibrateTable()
        elif self.key == Mma.kinect.calibrateGloveOpen:
            Mma.glove.calibrate(0)
        elif self.key == Mma.kinect.calibrateGloveClosed:
            Mma.glove.calibrate(1)
    def next(self, input):
        if self.key == Mma.kinect.calibrateBody:
            if Mma.kinect.isTableCalibrated():
                if Mma.glove.is_calibrated():
                    return Mma.calibrating
                else:print("Glove not calibrated.")
            else:print("Table not calibrated.")
        return Mma.neutral
    def on_start(self):
        #display depth image
        Mma.kinect.initDepth()


class Calibrating(State):
    def run(self):
        Mma.kinect.Calibrate()
    def next(self, input):
        if Mma.kinect.isCalibrationFinished():
            return Mma.waiting
        return Mma.calibrating
    def on_stop(self):
        Mma.kinect.killDepth()
    def on_start(self):
        Mma.kinect.initCalibration()
        
        
class Waiting(State):
    def run(self):
        time.sleep(0.01)
    def next(self, input):
        if Mma.glove.get_hand_position() == Mma.glove.fist:
            return Mma.marching
        return Mma.waiting
      
class Marching(State):
    def run(self):
        Mma.joystick.march()
    def next(self, input):
        if Mma.glove.get_hand_position == Mma.glove.open:
            return Mma.playing
        return Mma.marching
    def on_start(self):
        Mma.joystick.init()


class Playing(State):
    def run(self):
        Mma.joystick.update(Mma.glove.get_hand_position(), Mma.kinect.getArm())
    def next(self, input):
        if Mma.joystick.isParachuteOpened():
            return Mma.neutral
        return Mma.playing
    def on_stop(self):
        Mma.joystick.destroy()


class Mma(Machine):
    #init modules
    kinect = Kinect()
    joystick = Joystick(1)
    glove = Glove()
    manager = Manager()
    
    
    def __init__(self):
        # Initial state
        Machine.__init__(self, Mma.neutral)

# Static variable initialization:
Mma.neutral = Neutral()
Mma.calibrating = Calibrating()
Mma.waiting = Waiting()
Mma.playing = Playing()
Mma.marching = Marching()


#Mma().run()