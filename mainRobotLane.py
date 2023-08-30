from motorModule import Motor
from laneDetectionModule import getLaneCurve
import webcamModule
import cv2 as cv

##################################################
# motor = Motor(2, 3, 4, 17, 22, 27)
motor = Motor("P8_8", "P8_10", "P8_12", "P8_14", "P8_16", "P8_18")
##################################################


def main():
    img = webcamModule.getImg()
    curveVal = getLaneCurve(img, 1)  ## display value

    sen = 1.3  # SENSITIVITY
    maxVAl = 0.3  # MAX SPEED
    if curveVal > maxVAl:
        curveVal = maxVAl
    if curveVal < -maxVAl:
        curveVal = -maxVAl
    # print(curveVal)
    if curveVal > 0:
        sen = 1.7
        if curveVal < 0.05:
            curveVal = 0
    else:
        if curveVal > -0.08:
            curveVal = 0
    motor.move(0.20, -curveVal * sen, 0.05)  ## 1st par - base speed
    cv.waitKey(1)


if __name__ == "__main__":
    while True:
        main()
