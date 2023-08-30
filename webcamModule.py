import cv2 as cv

cap = cv.VideoCapture(0)


def getImg(display=False, size=[480, 240]):
    _, img = cap.read()
    img = cv.resize(img, (size[0], size[1]))
    if display:
        cv.imshow("IMG", img)
    return img


if __name__ == "__main__":
    while True:
        img = getImg(True)
