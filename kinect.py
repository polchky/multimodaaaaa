import freenect
import numpy as np
import cv2
import time
import imageutils
from glove import Glove


class Kinect:
    SIZE = (480, 640)
    CALIBRATION_SLEEP = 100
    CENTROID_STEP = 16
    KERNEL = np.ones((5, 5), np.uint8)
    ERODE_ITERATIONS = 8
    DILATE_ITERATIONS = 4

    def __init__(self):
        self.tmin = 0
        self.tmax = 220
        self.dmin = (np.inf, np.inf)
        self.dmax = (0, 0)
        self.origin = (0, 0)
        self.centroid = (0, 0)
        self.delta = (0, 0)
        self.direction = (0, 0)
        self.mask = np.zeros(Kinect.SIZE, np.uint8)
        self.raw = np.zeros(Kinect.SIZE, np.uint8)
        self.thresh = np.zeros(Kinect.SIZE, np.uint8)
        self.masked = np.zeros(Kinect.SIZE, np.uint8)
        self.calibrated = [False, False, False]
        self.parachute_state = 'closed'

    @staticmethod
    def get_raw():
        raw, _ = freenect.sync_get_depth()
        raw = imageutils.convert(raw)
        return raw

    def get_thresh(self, image):
        image = image.copy()
        image[image == 255] = 0
        image[image < self.tmin] = 0
        image[image > self.tmax] = 0
        image[image != 0] = 255
        return image

    @staticmethod
    def get_masked(image, mask):
        image = cv2.bitwise_and(image, image, mask=mask)
        return image

    def update(self):
        self.update_image()
        self.update_direction()

    def update_raw(self):
        self.raw = self.get_raw()

    def update_thresh(self):
        self.thresh = self.get_thresh(self.raw)

    def update_masked(self):
        self.masked = self.get_masked(self.thresh, self.mask)

    def update_image(self):
        self.update_raw()
        self.update_thresh()
        self.update_masked()

    def calibrate_mask(self, window, timer=3000):
        mask = np.zeros(Kinect.SIZE, np.uint8)
        n = timer / Kinect.CALIBRATION_SLEEP
        while timer > 0:
            self.update_image()
            mask += self.thresh / n
            self.display(window)
            cv2.waitKey(Kinect.CALIBRATION_SLEEP)
            timer -= Kinect.CALIBRATION_SLEEP

        c = imageutils.centroid(mask)
        threshold = mask[c[1], c[0]] * 0.8
        mask = cv2.threshold(mask, threshold, 255, cv2.THRESH_BINARY_INV)[1]
        mask = cv2.erode(mask, Kinect.KERNEL, Kinect.ERODE_ITERATIONS)
        mask = cv2.dilate(mask, Kinect.KERNEL, Kinect.DILATE_ITERATIONS)
        self.mask = mask
        self.calibrated[0] = True

    def calibrate_direction(self, window, timer=3000):
        xmin, ymin = (np.inf, np.inf)
        xmax, ymax = (0, 0)
        while timer > 0:
            self.update()
            self.display(window)
            x, y = self.delta
            xmin, ymin = min(xmin, x), min(ymin, y)
            xmax, ymax = max(xmax, x), max(ymax, y)
            cv2.waitKey(Kinect.CALIBRATION_SLEEP)
            timer -= Kinect.CALIBRATION_SLEEP
        self.dmin = xmin, ymin
        self.dmax = xmax, ymax
        self.calibrated[1] = True

    def update_centroid(self):
        self.centroid = imageutils.centroid(self.masked, Kinect.CENTROID_STEP)

    def update_direction(self):
        self.update_centroid()
        self.delta = self.get_delta()
        self.direction = self.get_direction()
        return self.centroid

    def get_delta(self):
        ox, oy = self.origin
        cx, cy = self.centroid
        return cx - ox, cy - oy

    def get_direction(self):
        x, y = self.delta
        xmin, ymin = self.dmin
        xmax, ymax = self.dmax
        return 1.*(x-xmin)/(xmax-xmin), 1.*(y-ymin)/(ymax-ymin)

    def set_threshold(self, tmin, tmax):
        self.tmin = tmin
        self.tmax = tmax

    def set_origin(self, origin=None):
        if origin is None:
            origin = self.centroid
        self.origin = origin
        self.arm_area = self.get_arm_area()
        self.calibrated[2] = True

    def update_parachute(self, hand_position):
        if hand_position != Glove.FINGER_POSITIONS['FIST']:
            self.parachute_state = 'closed'
            return
        self.update_image()
        arm_area = self.get_arm_area()
        print(arm_area)
        if self.parachute_state == 'closed' and arm_area < self.arm_area / 2:
            self.parachute_state = 'opening'
        elif self.parachute_state == 'opening' and arm_area > self.arm_area / 2:
            self.parachute_state = 'opened'
       
    def reset(self):
        self.parachute_state = 'closed'
        
    def get_arm_area(self):
        return sum(sum(self.masked[:,Kinect.SIZE[1]/2:]))
        
    def display(self,window):
        if self.calibrated[0]:
            cv2.imshow(window, self.masked)
        else:
            cv2.imshow(window, self.thresh)