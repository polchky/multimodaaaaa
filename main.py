# StateMachine/Mma1/MmaTest.py
# State Machine pattern using 'if' statements
# to determine the next state.
from kinect import Kinect
from glove import Glove
from machine import State, Machine
from joystick import Joystick
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
    def next(self):
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
    def next(self):
        if Mma.kinect.isCalibrationFinished():
            return Mma.waiting
        return Mma.calibrating
    def on_stop(self):
        Mma.kinect.killDepth()
    def on_start(self):
        Mma.kinect.initCalibration()
        
        
class Waiting(State):
    def next(self, input):
        if Mma.glove.get_hand_position() == Mma.glove.FINGER_POSITIONS['FIST']:
            return Mma.walking
        return Mma.waiting
      
class Walking(State):
    def run(self):
        Mma.joystick.walk(Mma.glove.get_hand_position())
    def next(self):
        if Mma.joystick.is_walking():
            return Mma.walking
        return Mma.playing


class Playing(State):
    def run(self):
        Mma.joystick.update_buttons(Mma.glove.get_hand_position())
        Mma.joystick.update_joystick(Mma.kinect.get_delta())
    def next(self):
        if Mma.joystick.is_parachute_opened():
            return Mma.neutral
        return Mma.playing

class Mma(Machine):
    #init modules
    kinect = Kinect()
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


#Mma().run()