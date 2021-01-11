import cv2
import numpy as np

# display webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640) #3->width
cap.set(4, 480) #4->height
cap.set(10, 150) #10->brightness

myColors = [[0, 200, 120, 20, 255, 255, "orange"],
            [23, 131, 70, 149, 255, 255, "yellow"]]
myColorValues = [[51, 153, 255],
                 [0, 255, 255]]
myPoints = []  # [x, y, colorID]


def findColor(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[:3])
        upper = np.array(color[3:6])
        # filter out colour of image
        mask = cv2.inRange(imgHSV, lowerb=lower, upperb=upper)
        x, y = getContours(mask)
        cv2.circle(imgResult, (x,y), 10, myColorValues[count], cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x, y, count])
        count += 1
        # cv2.imshow(color[-1], mask)
    return newPoints


def getContours(img):
    contours, hierarchy = cv2.findContours(img, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:  # minimum threshold to prevent noise
            # cv2.drawContours(imgResult, cnt, -1, (255,0,0), 3)  # -1 -> draw all contours
            # get curve length/perimeter to approximate corners of shapes
            peri = cv2.arcLength(cnt, closed=True)
            # getting coordinates of corner points
            approx = cv2.approxPolyDP(cnt, epsilon=0.02*peri, closed=True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2, y  # top center point


def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img, myColors, myColorValues)
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValues)

    cv2.imshow("Result", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


