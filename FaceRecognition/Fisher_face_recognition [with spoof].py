import cv2
import numpy as np
import os
import mysql.connector
import settings
import keras
from cv2 import dnn

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


recognizer = cv2.face.FisherFaceRecognizer_create()
recognizer.read('C:/Users/20307975/Desktop/opencv_project/FaceRecognition/trainer/Fishertrainer.yml')

cascadePath = cv2.data.haarcascades +"haarcascade_frontalface_default.xml"
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_eye.xml')
faceCascade = cv2.CascadeClassifier(cascadePath)

prototxt = 'C:/Users/20307975/Desktop/opencv_project/FaceRecognition/deploy.prototxt.txt'    
caffemodel='C:/Users/20307975/Desktop/opencv_project/FaceRecognition/res10_300x300_ssd_iter_140000.caffemodel'     
liveness_net =  cv2.dnn.readNetFromCaffe( prototxt, caffemodel)  



font = cv2.FONT_HERSHEY_SIMPLEX

# Define a function for liveness detection
def liveness_detection(img, gray_face):
    # Get the dimensions of the face bounding box
    x, y, w, h = gray_face

    # Extract the face from the frame
    face_image = img[y:y+h, x:x+w]

    # Preprocess the face image for liveness detection
    blob = cv2.dnn.blobFromImage(face_image, 1, (300, 300), (104, 177, 123), False, False)

    # Pass the face image through the liveness detector model
    liveness_net.setInput(blob)
    detections = liveness_net.forward()

    # Check if the liveness score is greater than the threshold
    liveness_score = detections[0, 0, 0, 2]
    if liveness_score > 0.9989:
        return True
    else:
        return False



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
            # Check if the face is live using liveness detection

            is_live = liveness_detection(img, (x, y, w, h))
            
            id, confidence = recognizer.predict(gray_face)

            confidence = confidence/1200
            confidence = (confidence)*100
            
            
            # Check if confidence is less them 100 ==> "0" is perfect match 
            if (confidence>40 and confidence<100):

                print(confidence)
                profile = getStudent(id)
                confidence = "  {0}%".format(round(confidence)) #100-80 =20%
                if (profile!=None):
                    id=profile[1]
        
                

            else:
                #print(confidence)
                #print(confidence)
                print(id)
                id = "unknown"
                confidence = "  {0}%".format(round(confidence))
            if is_live == False:
                id= "This is a spoof"
            
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