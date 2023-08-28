import cv2 as cv
import numpy as np
import utils


if __name__ == "__main__":
    cap = cv.VideoCapture("vid1.mp4")

    while True:
        status, img = cap.read()
        img = cv.resize(img, (480, 240))
        cv.imshow("Output", img)
        cv.waitKey(1)
