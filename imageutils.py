import cv2
import numpy as np


def convert(image):
    np.clip(image, 0, 2 ** 10 - 1, image)
    image >>= 2
    image = image.astype(np.uint8)
    return image


def resize(image, factor):
    image = cv2.resize(image, None,
                       fx=factor, fy=factor,
                       interpolation=cv2.INTER_NEAREST)
    return image


def centroid(image, step=1):
    h, w = image.shape
    arr = image[::step, ::step]
    white = arr > 0
    yy, xx = np.mgrid[0:h:step, 0:w:step]
    c = [xx[white].mean(), yy[white].mean()]
    c = tuple(int(i) if not np.isnan(i) else 0 for i in c)
    return c

