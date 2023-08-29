import cv2 as cv
import numpy as np


def thresholding(img):
    imgHsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    lowerWhite = np.array([80, 0, 0])
    upperWhite = np.array([255, 160, 255])
    maskWhite = cv.inRange(imgHsv, lowerWhite, upperWhite)
    return maskWhite


def warpImg(img, points, w, h):
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    matrix = cv.getPerspectiveTransform(pts1, pts2)
    imgWarp = cv.warpPerspective(img, matrix, (w, h))
    return imgWarp


def nothing(a):
    pass


def initializeTrackbars(intialTracbarVals, wT=480, hT=240):
    cv.namedWindow("Trackbars")
    cv.resizeWindow("Trackbars", 360, 240)
    cv.createTrackbar("Width Top", "Trackbars", intialTracbarVals[0], wT // 2, nothing)
    cv.createTrackbar("Height Top", "Trackbars", intialTracbarVals[1], hT, nothing)
    cv.createTrackbar(
        "Width Bottom", "Trackbars", intialTracbarVals[2], wT // 2, nothing
    )
    cv.createTrackbar("Height Bottom", "Trackbars", intialTracbarVals[3], hT, nothing)


def valTrackbars(wT=480, hT=240):
    widthTop = cv.getTrackbarPos("Width Top", "Trackbars")
    heightTop = cv.getTrackbarPos("Height Top", "Trackbars")
    widthBottom = cv.getTrackbarPos("Width Bottom", "Trackbars")
    heightBottom = cv.getTrackbarPos("Height Bottom", "Trackbars")
    points = np.float32(
        [
            (widthTop, heightTop),
            (wT - widthTop, heightTop),
            (widthBottom, heightBottom),
            (wT - widthBottom, heightBottom),
        ]
    )
    return points


def drawPoints(img, points):
    for x in range(4):
        cv.circle(
            img, (int(points[x][0]), int(points[x][1])), 15, (0, 0, 255), cv.FILLED
        )
    return img


def getHistogram(img, minPer=0.1, display=False):
    histValues = np.sum(img, axis=0)
    print(histValues)
    maxValue = np.max(histValues)
    # print(maxValue)
    minValue = minPer * maxValue

    indexArray = np.where(histValues >= minValue)
    basePoint = int(np.average(indexArray))
    print(basePoint)

    if display:
        imgHist = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
        for x, intensity in enumerate(histValues):
            cv.line(
                imgHist,
                (x, img.shape[0]),
                (x, img.shape[0] - round(intensity // 255)),
                (255, 0, 255),
                1,
            )
            cv.circle(imgHist, (basePoint, img.shape[0]), 20, (0, 255, 255), cv.FILLED)
        return basePoint, imgHist
    return basePoint
