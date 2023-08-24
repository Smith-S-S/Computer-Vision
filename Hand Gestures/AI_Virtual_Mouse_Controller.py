#in ths we use opencv and HandTrackingModuleX to take the cordinates of the hand
# And to control the mouse we use autopy 


import cv2
import numpy as np
import HandTrackingModuleX as htm
import time
import autopy

#######################
wCam, hCam = 640, 480
frameR = 100  # Frame Reduction (for that rectangle)
smoothening = 7
#########################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()
# print(wScr, hScr)

while True:
    # 1. Find hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)


    # 2. Get the tip of the index and middle fingers

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:] # here we are taking the x1,y1 value leaving the index
        x2, y2 = lmList[12][1:]
        # print(x1, y1, x2, y2)


        # 3. Check which fingers are up

        fingers = detector.fingersUp()
        # print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                      (255, 0, 255), 2)
        """
        (frameR,frameR) ---------  
                |               |
                |               |
                |               |
                -----   --- (wCam - frameR, hCam - frameR)
        """

        # 4. Only Index Finger : Moving Mode
        length_2, img, lineInfo = detector.findDistance(4, 5, img)
        length, img, lineInfo = detector.findDistance(3, 5, img)


        if fingers[1] == 1 and fingers[0] == 1:
            # fingers=[1,0,1,1,1]
            # fingers[1] its value is 0

            # 5. Convert Coordinates

            # because i give the values for the
            # full screen it is tough so we need to convert it

            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            #here it helps to take the xy points

            # 6. Smoothen Values

            clocX = plocX + (x3 - plocX) / smoothening
            # saying 0 to 100 values directly we are diluting and give to the
            clocY = plocY + (y3 - plocY) / smoothening
            # basically we are reducing

            # 7. Move Mouse

            # autopy.mouse.move(x3, y3) # if we go right it left we need to flip
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # 8. Both Index and middle fingers are up : Clicking Mode

        if fingers[1] == 1 and (length < 40 or length_2 <40):
            cv2.circle(img, (lineInfo[4], lineInfo[5]),
                       15, (0, 255, 0), cv2.FILLED)
            autopy.mouse.click()
            """
            # 9. Find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
            print(length)
            # 10. Click mouse if distance short
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]),
                           15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()  """

    # 11. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
    # 12. Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)
