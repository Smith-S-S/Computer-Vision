# importing the basic

import cv2
import cvzone
import numpy as np
from cvzone. FaceMeshModule import FaceMeshDetector
# opening the webcam
web= cv2.VideoCapture(0)
model= FaceMeshDetector(maxFaces=1) #creating the model
while True:
    success, img= web.read()
    img,face=model.findFaceMesh(img,draw=True)
    text_page= np.zeros_like(img) # for the black board
  
    if face:
        faced=face[0]
        pointL=faced[144]
        pointR=faced[374]

        #Finding the focal length
        w,_= model.findDistance(pointL,pointR)
        W=6.3
        #d=50
        #f=(w*d)/W
        #print (f)

        #focal length
        """we 1st finding the focal length 
        so we need to comment the above"""
        #finding the distance


        cv2.circle(img,pointL,5,(255,0,0),cv2.FILLED)
        cv2.circle(img, pointR, 5, (255, 0, 0), cv2.FILLED)
        cv2.line(img,pointR,pointL,(0,0,255),5,cv2.FILLED)

        f = 840
        d = (W * f) / w
        print(d)
        cvzone.putTextRect(img,f"Distance: {int(d)}cm",
                           (faced[10][0]-100,faced[10][1]-50),scale=2)

    # now we are going to stack them together

    image_stack= cvzone.stackImages([img,text_page],2,1)

    cv2.imshow("smith",image_stack)
    key=cv2.waitKey(1)

    if key ==32:
        break
