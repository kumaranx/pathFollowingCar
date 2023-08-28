import cv2 as cv
import numpy as np
import utils


def getLaneCurve(img):
    imgThresh = utils.thresholding(img)
    cv.imshow("Thresh image", imgThresh)

    return None


if __name__ == "__main__":
    cap = cv.VideoCapture("vid1.mp4")

    while True:
        status, img = cap.read()
        img = cv.resize(img, (480, 240))
        getLaneCurve(img)
        cv.imshow("Output", img)
        cv.waitKey(1)
