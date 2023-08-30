import cv2 as cv
import numpy as np
import utils

curveList = []
avgVal = 10


def getLaneCurve(img, display=2):
    imgCopy = img.copy()
    imgResult = img.copy()

    ## Step 1 - Thresholding - to extract the path
    imgThresh = utils.thresholding(img)

    ## Step 2 - Warping - to warp the path in birds eye view
    wT, hT, c = img.shape
    points = utils.valTrackbars()
    imgWarp = utils.warpImg(imgThresh, points, wT, hT)
    imgWarpResized = cv.resize(imgWarp, (480, 240))
    imgResize = cv.resize(imgCopy, (480, 240))
    imgWarpPoints = utils.drawPoints(imgResize, points)

    ## Step 3 - Histogram
    midPoint, imgHist = utils.getHistogram(
        imgWarpResized, display=True, minPer=0.5, region=4
    )

    curveAvgPoint, imgHist = utils.getHistogram(
        imgWarpResized, display=True, minPer=0.9
    )
    curveRaw = curveAvgPoint - midPoint

    ## Step 4 - Averaging
    curveList.append(curveRaw)
    if len(curveList) > avgVal:
        curveList.pop(0)
    curve = int(sum(curveList) / len(curveList))

    ## Step 5 - Display

    if display != 0:
        imgInvWarp = utils.warpImg(imgWarp, points, wT, hT, inv=True)
        imgInvWarp = cv.cvtColor(imgInvWarp, cv.COLOR_GRAY2BGR)
        imgInvWarp[0 : hT // 3, 0:wT] = 0, 0, 0
        # imgLaneColor = np.zeros_like(img)
        imgLaneColor = np.zeros_like(img)
        imgLaneColor = cv.resize(
            imgLaneColor, (imgInvWarp.shape[1], imgInvWarp.shape[0])
        )

        # imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv.bitwise_and(imgInvWarp, imgLaneColor)

        imgResult = cv.resize(imgResult, (imgInvWarp.shape[1], imgInvWarp.shape[0]))

        imgResult = cv.addWeighted(imgResult, 1, imgLaneColor, 1, 0)
        midY = 450
        cv.putText(
            imgResult,
            str(curve),
            (wT // 2 - 80, 85),
            cv.FONT_HERSHEY_COMPLEX,
            2,
            (255, 0, 255),
            3,
        )
        cv.line(
            imgResult, (wT // 2, midY), (wT // 2 + (curve * 3), midY), (255, 0, 255), 5
        )
        cv.line(
            imgResult,
            ((wT // 2 + (curve * 3)), midY - 25),
            (wT // 2 + (curve * 3), midY + 25),
            (0, 255, 0),
            5,
        )
        for x in range(-30, 30):
            w = wT // 20
            cv.line(
                imgResult,
                (w * x + int(curve // 50), midY - 10),
                (w * x + int(curve // 50), midY + 10),
                (0, 0, 255),
                2,
            )
        # fps = cv.getTickFrequency() / (cv.getTickCount() - timer)
        # cv.putText(
        #     imgResult,
        #     "FPS " + str(int(fps)),
        #     (20, 40),
        #     cv.FONT_HERSHEY_SIMPLEX,
        #     1,
        #     (230, 50, 50),
        #     3,
        # )
    if display == 2:
        imgStacked = utils.stackImages(
            0.7, ([img, imgWarpPoints, imgWarp], [imgHist, imgLaneColor, imgResult])
        )
        cv.imshow("ImageStack", imgStacked)
    elif display == 1:
        cv.imshow("Result", imgResult)

    ## Normalization
    curve = curve / 100
    if curve > 1:
        curve == 1
    if curve < -1:
        curve == -1

    # cv.imshow("Thresh image", imgThresh)
    # cv.imshow("Warp image", imgWarp)
    # cv.imshow("Warp Resized image", imgWarpResized)
    # cv.imshow("Warp Points image", imgWarpPoints)
    # cv.imshow("Histogram image", imgHist)

    return curve


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
        imgResized = cv.resize(img, (300, 280))
        curve = getLaneCurve(imgResized, display=0)
        print(curve)
        # cv.imshow("Output", img)
        cv.waitKey(1)
