import cv2
import numpy as np


def bright(image, gamma, b=0):
    rows, cols, channels = image.shape
    blank = np.zeros([rows, cols, channels], image.dtype)
    rst = cv2.addWeighted(image, gamma, blank, 1 - gamma, b)
    return rst


def blur(image, kernel_size):
    return cv2.blur(image, (kernel_size, kernel_size))