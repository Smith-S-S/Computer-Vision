#in this method we take list operation to take image from image files
import numpy
import cv2
import face_recognition
import os
import imutils

from datetime import datetime
import numpy as np

path = "atten_2"
images = []
class_name = []

my_list = os.listdir(path)
my_list=my_list[1:]
print(my_list)
print (path)

""" here we load the image to the image[] list """
for i in my_list:
    current_inage =cv2.imread(f"{path}/{i}")
    images.append(current_inage)
    class_name.append(os.path.splitext(i)[0])
print (class_name)

# function to create the face_encodings

def Find_encding(images):
    encode_list=[] # all the encodings
    for j in images:
        j = cv2.cvtColor(j, cv2.COLOR_BGR2RGB)
        face_encode = face_recognition.face_encodings(j)[0] #we are sending the one image we use [0]
        encode_list.append(face_encode)
    return encode_list


#function to create mark attendance

def markattendance(name):
    with open("attendance.csv","r+") as f: #we need to read and write so r+
        my_attendance= f.readlines() #read line by line

        name_list=[]
        for lines in my_attendance:
            entries = lines.split(",")
            name_list.append(entries[0]) #gives only the name
        if name not in name_list: # it help to avoid the reputations in the list
            now= datetime.now()
            dt_string=now.strftime("%H:%M:%S")
            f.writelines(f'\n{name},{dt_string}')



# First you have the digitized picture

encodings_list = Find_encding(images)
#print (encodings_list[0])
print ("Encoding Complete")

# to find the matches in our encodings with the web camp
cam= cv2.VideoCapture(0)
while True:
    success,img= cam.read()
    imgS = imutils.resize(img, width=400)  # rezising
    #imgS = cv2.resize(img,(0,0),None,0.25,0.25) #small image
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_in_current_img = face_recognition.face_locations(imgS) #in video we need to find the face in multiple location
    face_encode_face_in_current_img  = face_recognition.face_encodings(imgS,face_in_current_img)

#finding the matches

    for encode,location in zip(face_encode_face_in_current_img,face_in_current_img): #same loop we use zip to do 2 itrater
        matches = face_recognition.compare_faces(encodings_list,encode)
        face_dis= face_recognition.face_distance(encodings_list,encode) # it gives as 3 value because we have 3 known faces
        # and the lower the value good
        print(face_dis)
        # now we take index of the lowest image
        matches_index= np.argmin((face_dis))


        if matches[matches_index]:
            print ("matches: ",matches[matches_index])
            name=class_name[matches_index].upper()
            print (name)
            y1,x2,y2,x1=location
            cv2.rectangle(img,(location[3],location[0]),(location[1],location[2]),(255,8,23),2)

            cv2.putText(img, f"{name} {round(face_dis[0],2)}",(x1,y2),cv2.FONT_HERSHEY_SIMPLEX,1,(255,3,5),2)
            markattendance(name)

    cv2.imshow("sm",img)
    cv2.waitKey(1)



