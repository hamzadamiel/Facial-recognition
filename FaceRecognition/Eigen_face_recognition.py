import cv2
import numpy as np
import os
import mysql.connector
import settings


def getStudent(id):
  
    mycursor = settings.mydb.cursor()
    #mycursor = settings.mydb.reconnect()
    mycursor.execute("SELECT * FROM students WHERE s_id= "+str(id) )
    profile =None
    for row in mycursor:
        profile = row
    #mydb.close()
    return profile

old_path  = os.path.dirname(os.path.realpath(__file__))
old_path = old_path.replace("\\","/")
print(old_path)
path = old_path+ "/dataset"
recognizer = cv2.face.EigenFaceRecognizer_create()
recognizer.read('C:/Users/20307975/Desktop/opencv_project/FaceRecognition/trainer/Eigentrainer.yml')
cascadePath = cv2.data.haarcascades +"haarcascade_frontalface_default.xml"
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_eye.xml')
faceCascade = cv2.CascadeClassifier(cascadePath)

font = cv2.FONT_HERSHEY_SIMPLEX

result_file = open("result_eigen.txt", "w")


# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)
id= 0
confidence=0
while True:

    ret, img =cam.read()

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.3,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        gray_face = cv2.resize((gray[y: y+h, x: x+w]), (110, 110)) 

        gray_face = cv2.equalizeHist(gray_face)
        eyes = eye_cascade.detectMultiScale(gray_face)
        for (ex, ey, ew, eh) in eyes:
            id, confidence = recognizer.predict(gray_face)

            confidence = confidence/4200
            confidence = (confidence)*100
            # Check if confidence is less them 100 ==> "0" is perfect match 
            if (confidence>35 and confidence<100):

                print(confidence)
                profile = getStudent(id)
                confidence = "  {0}%".format(round(confidence)) #100-80 =20%
                if (profile!=None):
                    id=profile[1]
                    with open('result_eigen.txt', 'a') as file:
                        file.write(f'{id}, {confidence}\n')
        
                

            else:
                #print(confidence)
                #print(confidence)
                print(id)
                id = "unknown"
                confidence = "  {0}%".format(round(confidence))
            
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
        
  
    
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()