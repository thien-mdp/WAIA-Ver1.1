import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import cv2
from random import randrange
import os
#Folder Dataset
FOLDER = "dataset/"

class MyVideoCapture:
    def __init__(self):
        self.video = cv2.VideoCapture(0,0)
        if not self.video.isOpened():
            raise ValueError("Unable to open video source", 0)
        self.width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def __del__(self):
        if self.video.isOpened():
            self.video.release()

    def get_frame(self):
        if self.video.isOpened():
            ret, frame = self.video.read()
            frame = cv2.resize(frame, (640, 480))
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.frame = None
        self.create_video_frame()
        self.delay = 1

    def video_stream(self):
        _, frame = self.cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_frame.imgtk = imgtk
        self.video_frame.configure(image=imgtk)
        self.video_frame.after(1, self.video_stream)
    def update(self):
        ret, self.frame = self.video_frame.get_frame()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.video.after(1,self.update)
    def create_video_frame(self):
        self.video = ttk.Frame(self)
        self.video_frame = MyVideoCapture()
        self.id = tk.StringVar()
        self.id = ttk.Entry(self.video,textvariable="Nhap ID Sinh Vien",width=30)
        self.id.grid(row=0,column=0)
        self.canvas = tk.Canvas(self.video,width=self.video_frame.width,height=self.video_frame.height)
        self.canvas.grid(row = 0, column = 1)
        self.button_chup = ttk.Button(self.video,text="Chụp Anh",command=self.chup_anh)
        self.button_chup.grid(row = 1,column=0)
        self.update()
        self.video.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)
    def chup_anh(self):
        id = self.id.get()
        try:
            os.mkdir(FOLDER+str(id))
        except:
            pass
        # name_img = FOLDER+str(id) +"img"+str(randrange(1000,10000))+".jpg"
        name_img = FOLDER+str(id)+"/"+"img"+str(randrange(1000,10000))+".jpg"
        print(name_img)
        print(self.frame)
        status = cv2.imwrite(name_img,self.frame)
        print(status)
if __name__ == '__main__':
    app = App()
    app.mainloop()
# root = Tk()
# # Create a frame
# app = Frame(root, bg="white")
# app.grid()
# # Create a label in the frame
# lmain = Label(app)
# lmain.grid()
#
# # Capture from camera
# cap = cv2.VideoCapture(0)
#
# # function for video streaming
# def video_stream():
#     _, frame = cap.read()
#     cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
#     img = Image.fromarray(cv2image)
#     imgtk = ImageTk.PhotoImage(image=img)
#     lmain.imgtk = imgtk
#     lmain.configure(image=imgtk)
#     lmain.after(1, video_stream)
#
# video_stream()
# root.mainloop()