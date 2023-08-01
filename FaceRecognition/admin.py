import os
import cv2
import numpy as np
from tkinter import *
from PIL import Image
from PIL import Image
from add_data import AddStudentGUI
import os
import re
from pathlib import Path
from PIL import Image, ImageTk
import glob
import settings
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,Label
OUTPUT_PATH = Path(__file__).parent
#ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\20307975\Desktop\opencv_project\admin\build\assets\frame0")
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\20307975\Desktop\opencv_project\assets\frame0")

old_path  = os.path.dirname(os.path.realpath(__file__))
old_path = old_path.replace("\\","/")
print(old_path)
path = old_path+ "/dataset"
LBPHFace = cv2.face.LBPHFaceRecognizer_create()#create algorithms
FisherFace = cv2.face.FisherFaceRecognizer_create()
EigenFace = cv2.face.EigenFaceRecognizer_create()
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
"""
def getImagesAndLabels(self,path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L') # grayscale
        #PIL_img = PIL_img.resize((110,110))
        img_numpy = np.array(PIL_img,'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        img_numpy = cv2.equalizeHist(img_numpy, cv2.IMREAD_GRAYSCALE)
        faces = detector.detectMultiScale(img_numpy, 1.3,5)
        
        for (x,y,w,h) in faces:
            faceSamples.append(cv2.resize(img_numpy[y:y+h,x:x+w], (110,110)))
            ids.append(id)
    return faceSamples,ids

"""
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
#window = Tk()
class AdminGui:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1440x1024")
        self.master.configure(bg="#C5F1FF")
        self.master.attributes('-toolwindow', True) # remove maximize and minimize buttons
        self.master.geometry("+{}+{}".format(250, 0)) # set window location
        self.path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "dataset")
        self.LBPHFace = cv2.face.LBPHFaceRecognizer_create()
        self.FisherFace = cv2.face.FisherFaceRecognizer_create()
        self.EigenFace = cv2.face.EigenFaceRecognizer_create()
        self.detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.window= None
        #create canvas
        self.canvas = Canvas(
            self.master,
            bg="#C5F1FF",
            height=1024,
            width=1440,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(
            113.0,
            184.0,
            1326.0,
            841.0,
            fill="#E1F9FF",
            outline=""
        )
        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            720.0,
            271.0,
            image=self.image_image_1
        )
        print(self.image_image_1)
        self.canvas.create_text(
            366.0,
            356.0,
            anchor="nw",
            text="Welcome admin",
            fill="#000000",
            font=("Inter", 96 * -1)
        )
        #create buttons
        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_new_window, 
            relief="flat"
        )
        self.button_1.place(
            x=585.0,
            y=552.0,
            width=269.0,
            height=174.0
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command= self.show_window,
            relief="flat"
        )
        self.button_2.place(
        x=965.0,
        y=552.0,
        width=259.7391357421875,
        height=174.0
        )

        self.button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        self.button_3 = Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.adddata(),
            relief="flat"
        )
        self.button_3.place(
            x=204.0,
            y=548.0,
            width=267.7724609375,
            height=174.0
        )

        self.master.mainloop()
        #self.show_window()


    
    def show_window(self):
        def del_student():
            del_id = entry.get()

            # Define the file pattern to match
            pattern = f"user.{del_id}.*"

            # Get a list of matching file paths
            files = glob.glob(os.path.join(path, pattern))

            # Delete each file
            for file in files:
                os.remove(file)

            # Delete the record from the database
            mycursor = settings.mydb.cursor()
            sql = "DELETE FROM students WHERE s_id = %s"
            val = (del_id,)
            mycursor.execute(sql, val)
            settings.mydb.commit()

        # Show the deletion confirmation window
            new_window = Toplevel(self.master)
            new_window.geometry("200x100")
            new_window.title("Deletion complete")
            Label(new_window, text="The student record has been deleted.").pack()
            Button(new_window, text="OK", command=new_window.destroy).pack()

        # Close the delete id window
            del_window.destroy()

        del_window = Toplevel(self.master)
        del_window.geometry("400x100")
        del_window.title("Delete Student ID")
        label = Label(del_window, text="Enter Student ID:")
        label.pack()
        entry = Entry(del_window)
        entry.pack()
        button = Button(del_window, text="Submit", command=del_student)
        button.pack()

    # Save a reference to the delete window so it can be closed later
        self.master.del_window = del_window

    def open_new_window(self):
        old_path  = os.path.dirname(os.path.realpath(__file__))
        old_path = old_path.replace("\\","/")
        path = old_path+ "/dataset"
        LBPHFace = cv2.face.LBPHFaceRecognizer_create()
        FisherFace = cv2.face.FisherFaceRecognizer_create()
        EigenFace = cv2.face.EigenFaceRecognizer_create()

        detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        # function to get the images and label data
        def getImagesAndLabels(path):
            imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
            faceSamples=[]
            ids = []
            # Loop over each image path
            for imagePath in imagePaths:
                PIL_img = Image.open(imagePath).convert('L') # grayscale
                #PIL_img = PIL_img.resize((110,110))
                img_numpy = np.array(PIL_img,'uint8')
                # Extract the ID from the file name
                id = int(os.path.split(imagePath)[-1].split(".")[1])
                img_numpy = cv2.equalizeHist(img_numpy, cv2.IMREAD_GRAYSCALE)
                faces = detector.detectMultiScale(img_numpy, 1.3,5)
                # Loop over each detected face
                for (x,y,w,h) in faces:
                    faceSamples.append(cv2.resize(img_numpy[y:y+h,x:x+w], (110,110)))# Resize the face region to a fixed size
                    ids.append(id)
            return faceSamples,ids

        #self.label.configure(text="Training faces. Please wait...")
        # Train the LBPH, Eigen, and Fisher face recognizers using the face samples and IDs
        faces,ids = getImagesAndLabels(path)
        LBPHFace.train(faces, np.array(ids))
        EigenFace.train(faces, np.array(ids))
        FisherFace.train(faces, np.array(ids))

        # Save the model into trainer/trainer.yml
        LBPHFace.write(old_path+ '/trainer/LBPHtrainer.yml')
        EigenFace.write(old_path+ '/trainer/Eigentrainer.yml') 
        FisherFace.write(old_path+ '/trainer/Fishertrainer.yml') 
        if not hasattr(self.window, 'new_window'):
            new_window = Toplevel(self.master)
            new_window.geometry("200x100")
            new_window.title("New Window")
            Label(new_window, text="Training complete").pack()
            Button(new_window, text="OK", command=new_window.destroy).pack()

        self.master.new_window = new_window  # store the reference to the new window in the main window object

    def adddata(self):
    #root = Tk()
        add_student_window = Toplevel(self.master)
# create an instance of the AddStudentGUI class
        add_student_window = AddStudentGUI(add_student_window)

# call the update method to ensure that the GUI window is fully initialized and displayed
        self.master.update()

# add a protocol to handle closing the window
        self.master.protocol("WM_DELETE_WINDOW", add_student_window.on_closing)
        self.master.mainloop()


#admin = AdminGui(window)
#window.mainloop()