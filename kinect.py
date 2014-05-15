import freenect
import numpy as np

import cv2

import imageutils
from glove import Glove
from constants import *


class Kinect:
    SIZE = (480, 640)
    CALIBRATION_SLEEP = 100
    CENTROID_STEP = 16
    KERNEL = np.ones((5, 5), np.uint8)
    ERODE_ITERATIONS = 8
    DILATE_ITERATIONS = 4

    def __init__(self):
        self.tmin = KINECT_TMIN
        self.tmax = KINECT_TMAX
        self.dmin = tuple(reversed(Kinect.SIZE))
        self.dmax = (0, 0)
        self.origin = (0, 0)
        self.centroid = (0, 0)
        self.delta = (0, 0)
        self.direction = (0, 0)
        self.arm_area = 0
        self.mask_center = (0, 0)
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

        self.mask_center = c = imageutils.centroid(mask)
        threshold = mask[c[1], c[0]] * MASK_THRESH_FACTOR
        mask = cv2.threshold(mask, threshold, 255, cv2.THRESH_BINARY_INV)[1]
        mask = cv2.erode(mask, Kinect.KERNEL, Kinect.ERODE_ITERATIONS)
        mask = cv2.dilate(mask, Kinect.KERNEL, Kinect.DILATE_ITERATIONS)
        self.mask = mask
        self.calibrated[0] = True
        self.calibrated[2] = False

        return True

    def calibrate_direction(self, window, timer=3000):
        if not self.calibrated[2]:
            print("ERROR: Must set origin first.")
            return False

        xmin, ymin = (+np.inf, +np.inf)
        xmax, ymax = (-np.inf, -np.inf)
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

        return True

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
        if not self.calibrated[1]:
            return (0, 0)
            
        delta = list(self.delta)
        for i in [0, 1]:
            if delta[i] > 0:
                delta[i] /= +1. * self.dmax[i]
            else:
                delta[i] /= -1. * self.dmin[i]

        return tuple(np.clip(delta, -1, 1))

    def set_origin(self, origin=None):
        if origin is None:
            origin = self.centroid
        self.origin = origin
        self.arm_area = self.get_arm_area()
        self.calibrated[2] = True
        return True

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
        c = self.mask_center[0]
        return self.masked[:, c:].sum()

    def display(self, window):
        if self.calibrated[0]:
            image = self.masked
        else:
            image = self.thresh
        
        direction = tuple([int(100*self.direction[i] + self.origin[i]) for i in (0,1)])
        directionText = [round(self.direction[i]*100)/100 for i in (0,1)]
        directionText = ["{:+.2f}".format(i) for i in directionText]
        
        cv2.circle(image, self.origin, 8, 127, -1)
        cv2.circle(image, self.origin, 6, 0, -1)
        cv2.circle(image, direction, 6, 200, -1)
        cv2.circle(image, self.dmax, 6, 200, -1)
        cv2.circle(image, self.dmin, 6, 200, -1)
        cv2.line(image, self.origin, direction, 255, 1)
        cv2.putText(image, str(directionText), (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
        cv2.imshow(window, image)

    @staticmethod
    def destroy_windows():
        cv2.destroyAllWindows()