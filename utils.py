import cv2 as cv
import numpy as np


def thresholding(img):
    imgHsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    lowerWhite = np.array([80, 0, 0])
    upperWhite = np.array([255, 160, 255])
    maskWhite = cv.inRange(imgHsv, lowerWhite, upperWhite)

    return maskWhite
