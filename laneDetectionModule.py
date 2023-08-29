import cv2 as cv
import numpy as np
import utils


def getLaneCurve(img):
    imgCopy = img.copy()

    ## Step 1 - Thresholding - to extract the path
    imgThresh = utils.thresholding(img)

    ## Step 2 - Warping - to warp the path in birds eye view
    w, h, c = img.shape
    points = utils.valTrackbars()
    imgWarp = utils.warpImg(imgThresh, points, w, h)
    imgWarpResized = cv.resize(imgWarp, (480, 240))
    imgWarpPoints = utils.drawPoints(imgCopy, points)

    ## Step 3 - Histogram
    basePoint, imgHist = utils.getHistogram(imgWarpResized, display=True)

    cv.imshow("Thresh image", imgThresh)
    cv.imshow("Warp image", imgWarp)
    cv.imshow("Warp Resized image", imgWarpResized)
    cv.imshow("Warp Points image", imgWarpPoints)
    cv.imshow("Histogram image", imgHist)

    return None


if __name__ == "__main__":
    cap = cv.VideoCapture("vid1.mp4")
    initialTrackbarVals = [102, 80, 20, 214]
    utils.initializeTrackbars(initialTrackbarVals)
    frameCounter = 0

    while True:
        frameCounter += 1
        if cap.get(cv.CAP_PROP_FRAME_COUNT) == frameCounter:
            cap.set(cv.CAP_PROP_POS_FRAMES, 0)
            frameCounter = 0

        status, img = cap.read()
        img = cv.resize(img, (480, 240))
        getLaneCurve(img)
        cv.imshow("Output", img)
        cv.waitKey(1)
