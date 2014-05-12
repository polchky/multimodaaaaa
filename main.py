# StateMachine/Mma1/MmaTest.py
# State Machine pattern using 'if' statements
# to determine the next state.
from kinect import Kinect
from glove import Glove
from joystick import Joystick
from machine import State, Machine
import time, cv2
# A different subclass for each state:

class Neutral(State):
    def run(self):
        Mma.kinect.update()
        Mma.kinect.display(self.window)
        self.key = cv2.waitKey(50)
        #for test only
        if self.key == ord('t'):
            time.sleep(2)
            Mma.kinect.calibrate_mask(self.window)
            print('ok')
            time.sleep(1)
            Mma.kinect.calibrate_direction(self.window)
            print('ok')
            time.sleep(1)
            Mma.kinect.update()
            Mma.kinect.set_origin()
            print('ok')
            self.key = ord('q')
        if self.key == ord('p'):
            Mma.kinect.tmax += 1
        elif self.key == ord('m'):
            Mma.kinect.tmax -= 1
        elif self.key == ord('o'):
            Mma.glove.calibrate(0)
            print('done')
        elif self.key == ord('f'):
            Mma.glove.calibrate(1)
            print('done')
        elif self.key == ord('k'):
            print('calibrating...')
            Mma.kinect.calibrate_mask(self.window)
            print('done')
        elif self.key == ord('d'):
            print('calibrating...')
            Mma.kinect.calibrate_direction(self.window)
            print('done')
        elif self.key == ord('c'):
            Mma.kinect.update()
            Mma.kinect.set_origin()  
            print('done')
    def next(self):
        if self.key == ord('q'):
            #if Mma.glove.is_calibrated() == False:
            #    print('Glove not calibrated\n')
            if all(Mma.kinect.calibrated):
                return Mma.waiting
            else:
                print('Kinect not calibrated')
        return Mma.neutral
    def on_start(self):
        self.window = cv2.namedWindow("body")
        print('entering neutral state')
        print('o\tcalibrate glove open\n' + 
        'f\tcalibrate glove closed\n' +
        'p\t increase depth\n' + 
        'm\t decrease depth\n' +
        'k\tcalibrate kinect\n' + 
        'c\tset centroid\n' + 
        'd\tset direction\n' +
        'q\tend calibration\n')        
    def on_stop(self):
        cv2.destroyAllWindows()
        Mma.kinect.destroy_windows()
class Waiting(State):
    def on_start(self):
        time.sleep(1)
    def next(self): 
        #if Mma.glove.get_hand_position() == Mma.glove.FINGER_POSITIONS['FIST']:
        #    return Mma.walking
        return Mma.waiting
    def run(self):
        Mma.kinect.update()
        Mma.joystick.update_joystick(Mma.kinect.get_direction())
      
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
        Mma.joystick.update(Mma.kinect.direction(), Mma.glove.get_hand_position)
    def next(self):
        Mma.kinect.update_parachute(Mma.glove.get_hand_position())
        if Mma.kinect.parachute_state == 'opened':
            return Mma.neutral
        return Mma.playing
    def on_start(self):
        print('entering playing state')
    def on_stop(self):
        Mma.joystick.open_parachute()
        Mma.kinect.reset()
        Mma.joystick.reset()

class Mma(Machine):
    #init modules
    kinect = Kinect()
    #glove = Glove(port = "/dev/ttyACM0")
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