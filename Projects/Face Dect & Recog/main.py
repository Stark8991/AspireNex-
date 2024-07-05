import cv2 as cv
import tkinter as tk
import os
from tkinter import filedialog
# face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
# face_cascade = cv.CascadeClassifier('./Resources/haarcascade_frontalface_default.xml')

try:
    face_cascade = cv.CascadeClassifier('./Resources/haarcascade_frontalface_default.xml')
    if face_cascade.empty():
        raise cv.error("Failed to load cascade classifier")
except Exception as e:
    face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
    print(e)


def readFrame(frame):
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))
    num_faces = len(faces)
    for (x,y,w,h) in faces:
        cv.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),1)
    frame = cv.flip(frame,1)
    cv.putText(frame, f'Persons: {num_faces}', (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (6, 208, 1), 2)
    frame = cv.resize(frame, (600,480))
    return frame



def startWebCam():
    cap = cv.VideoCapture(0)
    while True:
        detected, frame = cap.read()
        
        if detected is False:
            #can add some exception handling
            break
        cv.imshow('Face Detection', readFrame(frame))
        if cv.waitKey(1) & 0xFF==ord('q') or cv.getWindowProperty('Face Detection', cv.WND_PROP_VISIBLE) < 1:
            break
    cap.release()
    cv.destroyAllWindows()        


def uploadImage():
    img_path = filedialog.askopenfilename()
    frame = cv.imread(img_path)

    frame = readFrame(frame)
    
    cv.imshow('Detect Face', frame)

    while True:
        key= cv.waitKey(1) & 0xFF
        if key==ord('q') or cv.getWindowProperty('Detect Face', cv.WND_PROP_VISIBLE) < 1:
            break
    cv.destroyAllWindows()
    


def uploadVideo():
    video_path = filedialog.askopenfilename()
    video = cv.VideoCapture(video_path)

    if not video.isOpened():
        return
    
    while True:
        ret, frame = video.read()
        if not ret:
            break
        frame = readFrame(frame)
        cv.imshow('Detect Faces', frame)
        key = cv.waitKey(1) & 0xFF
        if key==ord('q') or cv.getWindowProperty('Detect Faces', cv.WND_PROP_VISIBLE)< 1:
            break
    video.release()
    cv.destroyAllWindows()




# Creating a new Main window

root = tk.Tk()
root.title("Face Detection Application")
root.geometry("600x300")
root.configure(bg="#f0f0f0")    

# Create a frame for the buttons
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=50)

# Add styling options for buttons
button_style = {
    'font': ('Helvetica', 12),
    'bg': '#4CAF50',
    'fg': 'white',
    'activebackground': '#45a049',
    'width': 20,
    'height': 2,
    'bd': 0,
    'relief': 'flat'
}

# Create buttons
camera_button = tk.Button(button_frame, text="Open Camera", command=startWebCam, **button_style)
camera_button.grid(row=0, column=0, pady=10, padx=10)

photo_button = tk.Button(button_frame, text="Upload Image", command=uploadImage, **button_style)
photo_button.grid(row=1, column=0, pady=10, padx=10)

video_button = tk.Button(button_frame, text="Upload Videos", command=uploadVideo, **button_style)
video_button.grid(row=2, column=0, pady=10, padx=10)




if __name__=="__main__":
 root.mainloop()


