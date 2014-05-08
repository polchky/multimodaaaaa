# StateMachine/Mma1/MmaTest.py
# State Machine pattern using 'if' statements
# to determine the next state.
from kinect import Kinect
from glove import Glove
from joystick import Joystick
from machine import State, Machine
import time
# A different subclass for each state:

class Neutral(State):
    def run(self):
        print('Enter input: ')
        self.key = raw_input()
        if self.key == 'o':
            Mma.glove.calibrate(0)
        elif self.key == 'f':
            Mma.glove.calibrate(1)
        elif self.key == 'k':
            pass
            #Mma.kinect.calibrate_mask()
        elif self.key == 'c':
            pass
            #Mma.kinect.update()
            #Mma.kinect.set_origin()
    def next(self):
        if self.key == 'n':
            if Mma.glove.is_calibrated() == False:
                print('Glove not calibrated\n')
            #elif Mma.kinect.centroid == (0,0):
            #    print('Kinect not calibrated\n')
            else:return Mma.waiting
        return Mma.neutral
    def on_start(self):
        print('entering neutral state')
        print('o\tcalibrate glove open\nf\tcalibrate glove closed\nk\tcalibrate kinect\nc\tset centroid\n')        

        
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
            Mma.joystick.open_parachute()
            return Mma.neutral
        return Mma.playing
    def on_start(self):
        print('entering playing state')
    def on_stop(self):
        Mma.joystick.end_game()

class Mma(Machine):
    #init modules
    #kinect = Kinect()
    glove = Glove(port = "/dev/ttyACM0")
    joystick = Joystick()
    
    def __init__(self):
        # Initial state
        Machine.__init__(self, Mma.neutral)

# Static variable initialization:
Mma.neutral = Neutral()
Mma.waiting = Waiting()
Mma.playing = Playing()
Mma.walking = Walking()


Mma().run()