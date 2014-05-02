# StateMachine/Mma1/MmaTest.py
# State Machine pattern using 'if' statements
# to determine the next state.
import string, sys, time
from kinect import Kinect
from glove import Glove
from joystick import Joystick
sys.path += ['./StateMachine', './Mouse']
from State import State
from StateMachine import StateMachine
from MouseAction import MouseAction
# A different subclass for each state:

class Neutral(State):
    def run(self):
        self.action = Mma.kinect.displayDepth()
        if self.action == Mma.kinect.calibrateTable:
            Mma.kinect.calibrateTable()
    def next(self, input):
        if self.action == Mma.kinect.calibrateBody:
            if Mma.kinect.isTableCalibrated():
                return Mma.calibrating
            else:
                print("Table not calibrated! ZBRAAA!")
        return Mma.neutral
    def onStop(self):
        return
    def onStart(self):
        #display depth image
        Mma.kinect.initDepth()


class Calibrating(State):
    def run(self):
        Mma.kinect.Calibrate()
    def next(self, input):
        if Mma.kinect.isCalibrationFinished():
            return Mma.waiting
        return Mma.calibrating
    def onStop(self):
        Mma.kinect.killDepth()
    def onStart(self):
        Mma.kinect.initCalibration()
        
        
class Waiting(State):
    def run(self):
        time.sleep(0.01)
    def next(self, input):
        if Mma.glove.get_hand_position() == Mma.glove.fist:
            return Mma.marching
        return Mma.waiting
    def onStop(self):
        return
    def onStart(self):
        return
  
      
class Marching(State):
    def run(self):
        Mma.joystick.march()
    def next(self, input):
        if Mma.glove.get_hand_position == Mma.glove.open:
            return Mma.playing
        return Mma.marching
    def onStop(self):
        return
    def onStart(self):
        Mma.joystick.init()


class Playing(State):
    def run(self):
        Mma.joystick.update(Mma.glove.get_hand_position(), Mma.kinect.getArm())
    def next(self, input):
        if Mma.joystick.isParachuteOpened():
            return Mma.neutral
        return Mma.playing
    def onStop(self):
        Mma.joystick.destroy()
    def onStart(self):
        return


class Mma(StateMachine):
    #init modules
    kinect = Kinect()
    joystick = Joystick(1)
    glove = Glove('lol', 9600)
    
    
    def __init__(self):
        # Initial state
        StateMachine.__init__(self, Mma.neutral)

# Static variable initialization:
Mma.neutral = Neutral()
Mma.calibrating = Calibrating()
Mma.waiting = Waiting()
Mma.playing = Playing()
Mma.marching = Marching()


Mma().run()