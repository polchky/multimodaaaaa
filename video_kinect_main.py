# StateMachine/Mma1/MmaTest.py
# State Machine pattern using 'if' statements
# to determine the next state.
import cv2, time

from constants import GLOVE_PORT

from video_kinect import Kinect
from glove import Glove
from joystick import Joystick
from machine import State, Machine


# A different subclass for each state:

class Neutral(State):
    recording = False
    def run(self):
        Mma.kinect.update()
        image = Mma.kinect.display()
        cv2.imshow("body", image)
        self.key = cv2.waitKey(10)
        # for test only
        """
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
        """
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
            print('calibrating mask...')
            if Mma.kinect.calibrate_mask(self.window):
                print('done')
        elif self.key == ord('d'):
            print('calibrating direction...')
            if Mma.kinect.calibrate_direction(self.window):
                print('done')
        elif self.key == ord('c'):
            Mma.kinect.update()
            if Mma.kinect.set_origin():
                print('done')
        elif self.key == ord('r'):
            print('recording')
            self.writer_raw = cv2.VideoWriter("videos/kinect_raw.avi",cv2.cv.CV_FOURCC(*"FMP4"),12,(640, 480))
            self.writer_color = cv2.VideoWriter("videos/kinect_color.avi",cv2.cv.CV_FOURCC(*"FMP4"),12,(640, 480))
            self.writer_thresh = cv2.VideoWriter("videos/kinect_tresh.avi",cv2.cv.CV_FOURCC(*"FMP4"),12,(640, 480))
            self.writer_mask = cv2.VideoWriter("videos/kinect_mask.avi",cv2.cv.CV_FOURCC(*"FMP4"),12,(640, 480))
            self.writer_masked = cv2.VideoWriter("videos/kinect_masked.avi",cv2.cv.CV_FOURCC(*"FMP4"),12,(640, 480))
            self.writer_complete = cv2.VideoWriter("videos/kinect_complete.avi",cv2.cv.CV_FOURCC(*"FMP4"),12,(640, 480))
            self.recording = True
        elif self.key == ord('s'):
            self.writer_color.release()
            self.writer_raw.release()
            self.writer_thresh.release()
            self.writer_mask.release()
            self.writer_masked.release()
            self.writer_complete.release()
            print('stop recording')
            self.recording = False
        if self.recording:
            self.writer_raw.write(cv2.cvtColor(Mma.kinect.get_raw(), cv2.COLOR_GRAY2RGB)) 
            self.writer_color.write(cv2.cvtColor(Mma.kinect.get_color(), cv2.COLOR_BGR2RGB)) 
            self.writer_thresh.write(cv2.cvtColor(Mma.kinect.thresh, cv2.COLOR_GRAY2RGB)) 
            self.writer_mask.write(cv2.cvtColor(Mma.kinect.mask, cv2.COLOR_GRAY2RGB)) 
            self.writer_masked.write(cv2.cvtColor(Mma.kinect.masked, cv2.COLOR_GRAY2RGB)) 
            self.writer_complete.write(cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)) 

    def next(self):
        if self.key == ord('q'):
            if not Mma.glove.is_calibrated():
                print('Glove not calibrated\n')
            if not all(Mma.kinect.calibrated):
                print('Kinect not calibrated')
            else:
                return Mma.waiting
        return self

    def on_start(self):
        self.window = cv2.namedWindow("body")
        print('entering neutral state')
        print('o\tcalibrate glove open\n' +
              'f\tcalibrate glove closed\n' +
              'p\t increase depth\n' +
              'm\t decrease depth\n' +
              'k\tcalibrate kinect\n' +
              'c\tset origin\n' +
              'd\tcalibrate direction\n' +
              'q\tend calibration\n')

    def on_stop(self):
        cv2.destroyAllWindows()


class Waiting(State):
    def next(self):
        if Mma.glove.get_hand_position() == Mma.glove.FINGER_POSITIONS['FIST']:
            return Mma.walking
        return self


class Walking(State):
    def run(self):
        Mma.joystick.walk(Mma.glove.get_hand_position())

    def next(self):
        if Mma.joystick.is_walking():
            return self
        return Mma.playing


class Playing(State):
    def run(self):
        Mma.kinect.update()
        Mma.joystick.update(Mma.kinect.get_direction(), Mma.glove.get_hand_position())

    def next(self):
        Mma.kinect.update_parachute(Mma.glove.get_hand_position())
        if Mma.kinect.parachute_state == 'opened':
            return Mma.neutral
        return self

    def on_stop(self):
        Mma.joystick.open_parachute()
        Mma.kinect.reset()
        Mma.joystick.reset()


class Mma(Machine):
    # init modules
    kinect = Kinect()
    #glove = Glove(port=GLOVE_PORT)
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