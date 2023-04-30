import time
import cv2
import numpy as np
import mediapipe as mp
import HandTrackingModule as htm
import math


w,h=(120,120)
cam = cv2.VideoCapture(0)
cam.set(3,w)
cam.set(4,h)
c_time = 0
p_time = 0


# now
minVol=0
maxVol = 10
volBar=400
detector=htm.handDetector(detectionCon=0.5)

while True:
    _,img=cam.read()
    img=detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    lmList = list(lmList)
    lmList = lmList[0]
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        # now we want that line length to scale up and down the volume
        length = math.hypot(x2-x1,y2-y1)


        # volume 0 to 10
        # but our finger length 50 to 300

        vol = np.interp(length, [50, 300], [minVol, maxVol])
        volBar = np.interp(length, [50, 300], [400, 150]) # here the min id 400 and the max is 150
        volPer = np.interp(length, [50, 300], [0, 100])
        print(int(length), vol)

        if length <=50:
            cv2.circle(img, (cx, cy), 15, (0,255, 0), cv2.FILLED)

        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                    1, (255, 0, 0), 3)

    c_time=time.time()
    fps=1/(c_time-p_time)
    p_time= c_time

    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,255),3)
    cv2.imshow("im", img)
    key=cv2.waitKey(1)
    if key == ord("s"):
        break
