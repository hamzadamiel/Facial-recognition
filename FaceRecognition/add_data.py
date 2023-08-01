from pathlib import Path
from tkinter import *
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import numpy as np
import tkinter as tk
from tkinter import messagebox
import cv2
import mysql.connector
import settings
import os
import glob
from PIL import Image, ImageTk
from admin import *
import sys


OUTPUT_PATH = Path(__file__).parent
#ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\20307975\Desktop\opencv_project\add_student\build\assets\frame0")
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\20307975\Desktop\opencv_project\assets\frame0")

face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
id = 1
file_count= 0

counter=0

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
# create a new Tkinter window

def create_student_popup(name, course):
    global counter
    response = tk.messagebox.askquestion("Create new student?", f"Sorry, {name} doesn't exist in the {course} course. Would you like to create a new student?")
    if response == "yes":
        mycursor = settings.mydb.cursor()
        course_query = "SELECT c_id FROM course WHERE c_name=%s"
        mycursor.execute(course_query, (course,))
        c_id_row = mycursor.fetchone()
        if c_id_row is not None:
            c_id_row = c_id_row[0]
            mycursor.execute("SELECT s_id FROM students ORDER BY s_id DESC LIMIT 1")
            last_row = mycursor.fetchone()[0]
            id = last_row+1

            id = tk.messagebox.showinfo("Id",f"The id for {name} is {str(id)}")
            query = "INSERT INTO students (name,c_id) VALUES (%s,%s)"
            mycursor.execute(query,(name,c_id_row))
            settings.mydb.commit()
            #adddata(id, name, img_count)
        else:
            response = tk.messagebox.showinfo("Course not recognised", f"Sorry {course} not recognised")

    else:
        response = tk.messagebox.showinfo("", f"Ok bye")
    top = Toplevel()
    # code to create widgets and layout
    top.destroy()
    #sys.exit()

def studentdetail(id,name,course):
    
    mycursor = settings.mydb.cursor()
    select_query = "SELECT * FROM students WHERE s_id=%s AND name=%s" #query to check if srudent exist
    mycursor.execute(select_query, (id, name))
    selected_rows = mycursor.fetchone()
    
    if selected_rows is not None:
        print(selected_rows)
        #adddata(id, name, img_count)
    else:
        create_student_popup(name,course)
class AddStudentGUI:

    def __init__(self, master):
        global img_count
        self.img_count = 0
        img_count = self.img_count
        img_count =0  
        self.master = master
        self.master.geometry("1440x1024")
        self.master.configure(bg="#C5F1FF")
        self.master.attributes('-toolwindow', True) # remove maximize and minimize buttons
        self.master.geometry("+{}+{}".format(250, 0)) # set window location

        self.canvas = Canvas( #create canvas
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
            12.0,
            180.0,
            733.0,
            998.0,
            fill="#FFFFFF",
            outline=""
        )

        self.image_image_1 = PhotoImage( #create images
            file=relative_to_assets("image_1.png")
        )
        self.image_1 = self.canvas.create_image(
            711.0,
            93.0,
            image=self.image_image_1
        )
        self.entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png")
        )
        self.entry_bg_1 = self.canvas.create_image(
            472.5,
            274.5,
            image=self.entry_image_1
        )

        self.entry_1 = Text(
            self.master,
            bd=0,
            font=("Arial", 20), # set the font to Arial, size 20
            bg="#E5E3E3",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_1.place(
            x=312.0,
            y=233.0,
            width=321.0,
            height=81.0
        )

        self.entry_image_2 = PhotoImage(
            file=relative_to_assets("entry_2.png")
        )
        self.entry_bg_2 = self.canvas.create_image(
            472.5,
            431.5,
            image=self.entry_image_2
        )
        self.entry_2 = Text(
            self.master,
            bd=0,
            bg="#E5E4E4",
            font=("Arial", 20), # set the font to Arial, size 20
            fg="#000716",
            highlightthickness=0
        )
        self.entry_2.place(
            x=312.0,
            y=390.0,
            width=321.0,
            height=81.0
        )

        self.canvas.create_text( 
            26.0,
            255.0,
            anchor="nw",
            text="Enter student id:",
            fill="#000000",
            font=("Inter", 32 * -1)
        )

        self.entry_image_3 = PhotoImage(
            file=relative_to_assets("entry_3.png")
        )
        self.entry_bg_3 = self.canvas.create_image(
            472.5,
            594.5,
            image=self.entry_image_3
        )
        self.entry_3 = Text(
            self.master,
            bd=0,
            bg="#E5E4E4",
            font=("Arial", 20), # set the font to Arial, size 20
            fg="#000716",
            highlightthickness=0
        )
        self.entry_3.place(
            x=312.0,
            y=553.0,
            width=321.0,
            height=81.0
        )

        self.entry_image_4 = PhotoImage(
            file=relative_to_assets("entry_3.png")
        )
        self.entry_bg_4 = self.canvas.create_image(
            472.5,
            594.5,
            image=self.entry_image_3
        )
        self.entry_4 = Text(
            self.master,
            bd=0,
            bg="#E5E4E4",
            font=("Arial", 20), # set the font to Arial, size 20
            fg="#000716",
            highlightthickness=0
        )
        self.entry_4.place(
            x=312.0,
            y=713.0,
            width=321.0,
            height=81.0
        )
        self.canvas.create_text(
        26.0,
        412.0,
        anchor="nw",
        text="Enter name:",
        fill="#000000",
        font=("Inter", 32 * -1)
        )
        
        self.canvas.create_text(
        26.0,
        558.0,
        anchor="nw",
        text="Enter Course:",
        fill="#000000",
        font=("Inter", 32 * -1)
        )

        self.canvas.create_text(
        26.0,
        720.0,
        anchor="nw",
        text="No. of photos taken:",
        fill="#000000",
        font=("Inter", 32 * -1)
        )

        self.canvas.create_rectangle(
        748.0,
        180.0,
        1424.0,
        998.0,
        fill="#76C6F2",
        outline="")

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("submit.png"))
        
        self.button_1 = Button(
            self.master,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: button1_clicked(),
            relief="flat"
        )
        self.button_1.place(
        x=170.0,
        y=834.0,
        width=303.0,
        height=155.0
        )
        
        # create a new canvas for displaying the camera feed
        self.camera_canvas = Canvas(
            self.master,
            bg="#76C6F2",
            height=640,
            width=480,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.camera_canvas.place(x=850, y=350)
        
        # create a video capture object
        self.video_capture = cv2.VideoCapture(0)

        # start a loop to capture and display frames

        # create a button for taking pictures
        """
        self.capture_button = Button(
            self.master,
            text="Take Pictures",
            command=self.capture_images
        )
        self.capture_button.place(x=200, y=860)
        """

        def button1_clicked():

            global id,name,course,amount
            id= self.entry_1.get("1.0", "end-1c")#store entries in variables
            name=self.entry_2.get("1.0", "end-1c")
            course = self.entry_3.get("1.0", "end-1c")
            amount = self.entry_4.get("1.0", "end-1c")
            if id =="" or name =="" or course =="" or amount=="" or amount.isdigit==False:
                missing = tk.messagebox.showinfo("Field missing",f"Sorry feids are missing or input is incorrect")
            else:

                studentdetail(id, name, course)
                #print(str(counter) + "lol this")
                self.capture_images()
                self.entry_1.delete("1.0", "end")#delete entry
                self.entry_2.delete("1.0", "end")
                self.entry_3.delete("1.0", "end")
                self.entry_4.delete("1.0", "end")
        self.update_camera()
        self.master.mainloop()
        
    def capture_images(self):
        global id, name, course, amount
        print(id)
        print(amount)
        # detect faces in the camera feed and save 10 images to a folder
        
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = dir_path.replace("\\","/")
        folder_path = dir_path + "/dataset/"
        print(folder_path)
        file_count = len([f for f in os.listdir(folder_path)])
        amount = int(amount)
        img_count = 0  # initialize img_count to 0
        face_count = 0
        pattern = folder_path+f"user.{id}.*.jpg"
        files = glob.glob(pattern)
        last_file = max(files, key=lambda f: int(f.split(".")[-2])) if files else None
        number = int(last_file.split(".")[-2]) + 1 if last_file else 1  # if there are no files, start from 1

        while face_count < amount and img_count < amount:  # fix loop condition
            # read a frame from the camera
            ret, frame = self.video_capture.read()

            # detect faces in the frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)

            # save an image for each detected face
            for (x,y,w,h) in faces:
                number += 1
                face_image = gray[y:y+h, x:x+w]
                cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
                cv2.imwrite(dir_path+"/dataset/user." + str(id) + '.' + str(number) + ".jpg", gray[y:y+h,x:x+w])
                print(dir_path+"/dataset/user." + str(id) + '.' + str(number) + ".jpg", gray[y:y+h,x:x+w])
                face_count += 1
                img_count += 1  # increment img_count

                if face_count == amount or img_count == amount:  # add condition to exit loop
                    break
            
                    
            # display the frame on the camera canvas
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (640, 480))
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image)
            self.camera_canvas.create_image(0, 0, anchor=NW, image=photo)
            self.camera_canvas.image = photo

            # update the GUI
            self.master.update_idletasks()

            # wait for a key press or timeout
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            #print("pictures taken")
        # release the video capture object
        #self.video_capture.release()

    def update_camera(self):
    # check if the root window is still valid
        if not self.master:
            return
        
    # read a frame from the camera
        ret, frame = self.video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        # save an image for each detected face
        for (x,y,w,h) in faces:

            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)

        if ret:
            # convert the frame to RGB format and resize it
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (640, 480))
            #cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
            # create a PIL image from the frame
            image = Image.fromarray(frame)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
        # save an image for each detected face
        # convert the PIL image to a Tkinter PhotoImage and display it on the camera canvas
            photo = ImageTk.PhotoImage(image)
            self.camera_canvas.create_image(0, 0, anchor=NW, image=photo)
            self.camera_canvas.image = photo

    # call the update_camera method again after 10 milliseconds
        self.master.after(10, self.update_camera)
        
    def on_closing(self):
        # Release the video file or capture device and close the window
        try:
            self.video_capture.release()
            self.master.destroy()
        except TclError:
            print("error")

#root = Tk()

# create an instance of the AddStudentGUI class
#add_student_window = AddStudentGUI(root)

# call the update method to ensure that the GUI window is fully initialized and displayed
#root.update()

# add a protocol to handle closing the window
#root.protocol("WM_DELETE_WINDOW", add_student_window.on_closing)

# run the Tkinter event loop
#root.mainloop()