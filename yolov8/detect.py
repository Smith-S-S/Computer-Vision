import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
import cvzone
import math
import time
new_frame_time=0
prev_frame_time=0
model = YOLO("C:/mac/pycham/pythonProject3/yolov8n.pt")
frame = cv2.VideoCapture(0)

#model.train(data='my_data.yaml', imgsz=[640, 480], rect=True)
# model.predict(source='images', imgsz=[640, 480], rect=True)



my_file =open("coco.txt","r")
df= my_file.read()
classNames= df.split("\n")


while True:
    ret, cam = frame.read()
    if not ret:
        break
    result= model.predict(source=cam)

    for r in result:
        boxes = r.boxes
        for box in boxes:
            # --------------  for box  ---------------
            #  for cv
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 5)
            #  for cvzone
            w, h = x2 - x1, y2 - y1
            cvzone.cornerRect(cam, (x1, y1, w, h), l=9, rt=5)
            # --------------  for confidance  ---------------
            con = math.ceil((box.conf[0] * 100)) / 100
            cls_name = int(box.cls[0])
            current_class = classNames[cls_name]
            cvzone.putTextRect(cam, f'Waste: {current_class}', (max(0, x1), max(35, y1)),
                               scale=2, thickness=3, offset=10)

    new_frame_time = time.time()
    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    print("FPS: ", int(fps))
    cv2.imshow("Debris Collector", cam)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cv2.destroyAllWindows()
