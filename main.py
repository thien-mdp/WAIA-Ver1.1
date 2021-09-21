import tkinter as tk
import googletts
from tkinter import messagebox
import cv2
import os
import time
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
import sqlite3
import FaceMaskDetector
import threading
# from send2trash import send2trash # (shutil delete permanently)


window = tk.Tk()
#helv36 = tk.Font(family='Helvetica', size=36, weight='bold')
window.title("HỆ THỐNG NHẮC NHỞ ĐEO KHẨU TRANG")
window.geometry('1600x900')
dialog_title = 'Thoát'
dialog_text = 'Bạn muốn thoát?'
#answer = messagebox.askquestion(dialog_title, dialog_text)

# window.geometry('1280x720')
window.configure(background='#FFD700')

#window.attributes('-fullscreen', True)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)


message = tk.Label(window, text="HỆ THỐNG NHẮC NHỞ ĐEO KHẨU TRANG", bg="gray25",
                   fg="white", width=50, height=3, font=('times', 30, 'bold'))
message.place(x=200, y=20)

lbl = tk.Label(window, text="Nhập ID", width=20, height=2,
               fg="white", bg="gray25", font=('times', 15, ' bold '))
lbl.place(x=200, y=200)
txt = tk.Entry(window, width=20, bg="gray25",
               fg="white", font=('times', 15, ' bold '))
txt.place(x=500, y=215)

lbl2 = tk.Label(window, text="Nhập Tên", width=20, fg="white",
                bg="gray25", height=2, font=('times', 15, ' bold '))
lbl2.place(x=200, y=300)
txt2 = tk.Entry(window, width=20, bg="gray25",
                fg="white", font=('times', 15, ' bold '))
txt2.place(x=500, y=315)

lblRole = tk.Label(window, text="Nhập Chức Vụ", width=20, height=2,
                   fg="white", bg="gray25", font=('times', 15, ' bold '))
lblRole.place(x=200, y=400)
txtRole = tk.Entry(window, width=20, bg="gray25",
                   fg="white", font=('times', 15, ' bold '))
txtRole.place(x=500, y=415)


lblNumberPhone = tk.Label(window, text="Nhập Số Điện Thoại", width=20,
                          height=2, fg="white", bg="gray25", font=('times', 15, ' bold '))
lblNumberPhone.place(x=850, y=200)
txtNumberPhone = tk.Entry(window, width=20, bg="gray25",
                          fg="white", font=('times', 15, ' bold '))
txtNumberPhone.place(x=1150, y=215)

lblAddress = tk.Label(window, text="Nhập Tên Lớp", width=20,
                      height=2, fg="white", bg="gray25", font=('times', 15, ' bold '))
lblAddress.place(x=850, y=300)
txtAddress = tk.Entry(window, width=20, bg="gray25",
                      fg="white", font=('times', 15, ' bold '))
txtAddress.place(x=1150, y=315)


lbl3 = tk.Label(window, text="Nhắc Nhở Vi phạm : ", width=20,
                fg="white", bg="gray25", height=3, font=('times', 15, ' bold '))
lbl3.place(x=250, y=650)
message2 = tk.Label(window, text="", fg="white", bg="gray25",
                    activeforeground="green", width=60, height=3, font=('times', 15, ' bold '))
message2.place(x=560, y=650)


def Insert(id, name, role, numPhone, address):
    conn = sqlite3.connect(
        "data.db")
    query = "SELECT * FROM Employee WHERE ID = " + str(id)
    cursor = conn.execute(query)

    isRecordExist = 0

    for row in cursor:
        isRecordExist = 1
    if isRecordExist == 0:
        query = "INSERT INTO Employee(ID, Name, Role, NumberPhone, Address) VALUES(" + str(id) + ", '" + str(
            name) + "', '" + str(role) + "', '" + str(numPhone) + "', '" + str(address) + "')"
        conn.execute(query)
        conn.commit()
        conn.close()
    else:
        messagebox.showwarning(
            "WARNING", "ID ĐÃ TỒN TẠI. VUI LÒNG NHẬP LẠI ID!!")


def delete(id, name, role, numPhone, address):

    conn = sqlite3.connect(
        "data.db")
    query = "SELECT * FROM Employee WHERE ID = " + str(id)
    cursor = conn.execute(query)

    isRecordExist = 0

    for row in cursor:
        isRecordExist = 1
    if isRecordExist == 1:
        # Delete in database
        query = "DELETE FROM Employee WHERE ID = " + str(id)
        conn.execute(query)
        conn.commit()
        conn.close()
        messagebox.showinfo("THÔNG BÁO", "XÓA THÀNH CÔNG!")
    else:
        messagebox.showwarning(
            "WARNING", "NHÂN VIÊN NÀY KHÔNG ĐƯỢC LƯU TRỮ TRONG DANH SÁCH!!")


def clear():
    # Clear ID
    txt.delete(0, 'end')
    res = ""
    # Clear Name
    txt2.delete(0, 'end')
    res = ""
    # Clear Role
    txtRole.delete(0, 'end')
    res = ""
    # Clear NumberPhone
    txtNumberPhone.delete(0, 'end')
    res = ""
    # Clear Address
    txtAddress.delete(0, 'end')
    res = ""


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


def is_empty(a):
    return len(a) == 0


def Add():
    Id = (txt.get())
    name = (txt2.get())
    if is_number(Id) == False:
        messagebox.showwarning("WARNING", "VUI LÒNG NHẬP ID LÀ MỘT SỐ!")
    elif name == "":
        messagebox.showwarning('WARNING', "VUI LÒNG NHẬP TÊN NHÂN VIÊN!")
    elif (is_number(Id) and is_empty(name) == 0):
        # Load TVien NDKM cua OpenCV
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        # Truy cap den camera cua laptop
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        # insert to DB
        id = txt.get()
        name = txt2.get()
        role = txtRole.get()
        numPhone = txtNumberPhone.get()
        address = txtAddress.get()

        conn = sqlite3.connect(
            "data.db")
        query = "SELECT * FROM Employee WHERE ID = " + str(Id)
        cursor = conn.execute(query)

        isRecordExist = 0

        for row in cursor:
            isRecordExist = 1
        if isRecordExist == 0:
            query = "INSERT INTO Employee(ID, Name, Role, NumberPhone, Address) VALUES(" + str(id) + ", '" + str(
                name) + "', '" + str(role) + "', '" + str(numPhone) + "', '" + str(address) + "')"
            conn.execute(query)
            conn.commit()
            conn.close()

            # Sau khi insert vao database thi se chup anh de train
            sampleNum = 0

            # Lay du lieu tu camera
            while (True):
                ret, frame = cap.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                for x, y, w, h in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h),
                                  (0, 225, 0), 2)

                    if not os.path.exists('TrainingImage/Image_' + Id):
                        os.makedirs('TrainingImage/Image_' + Id)

                    sampleNum += 1
                    cv2.imwrite('TrainingImage/Image_' + Id + '/User.' + str(id) +
                                '.' + str(sampleNum) + '.jpg', gray[y: y + h, x: x + w])

                cv2.imshow('frame', frame)
                cv2.waitKey(1)

                if sampleNum > 100:
                    break
            cap.release()
            cv2.destroyAllWindows()

            # Training Image
            path = 'TrainingImage/Image_' + Id
            recognizer = cv2.face_LBPHFaceRecognizer.create()
            faces, Ids = getImageWithId(path)
            if not os.path.exists('Training'):
                os.makedirs('Training')
            if os.path.exists("Training/haarcascade_frontalface.xml"):
                recognizer.read("Training/haarcascade_frontalface.xml")
                recognizer.update(faces, np.array(Ids))
                recognizer.save('Training/haarcascade_frontalface.xml')
            else:
                recognizer.train(faces, np.array(Ids))
                recognizer.save('Training/haarcascade_frontalface.xml')
            cv2.destroyAllWindows()

            messagebox.showinfo("THÔNG BÁO", "THÊM NHÂN VIÊN THÀNH CÔNG!")

        else:
            messagebox.showwarning(
                "WARNING", "ID ĐÃ TỒN TẠI. VUI LÒNG NHẬP LẠI ID!!")


# path = 'TrainingImage'
def getImageWithId(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # print(imagePaths)
    faces = []
    IDs = []

    for imagePath in imagePaths:
        faceImg = Image.open(imagePath).convert('L')
        faceNp = np.array(faceImg, 'uint8')
        # print(faceNp)
        Id = int(imagePath.split('\\')[1].split('.')[1])
        faces.append(faceNp)
        IDs.append(Id)
        # cv2.imshow("Trainning", faceNp)
        cv2.waitKey(10)
    return faces, IDs

# Ham lay id da dc luu o Sql Little


def getProfile(Id):
    conn = sqlite3.connect(
        "data.db")
    query = "SELECT * FROM Employee WHERE ID="+str(Id)
    cursor = conn.execute(query)
    profile = None
    for row in cursor:
        profile = row
    conn.close()
    return profile


def TrackImages():
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    # Doc File
    if os.path.exists("Training/haarcascade_frontalface.xml"):
        recognizer.read("Training/haarcascade_frontalface.xml")
    else:
        print('zxcz')
        recognizer.read("../haarcascade_frontalface_default.xml")

    # Mo camera man hinh laptop
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # cap = video.create_capture(0)
    font = cv2.FONT_HERSHEY_COMPLEX
    col_names = ['Id', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)
    faceMask = FaceMaskDetector.FaceMask()

    length = 0
    while True:
        _ret, frame = cap.read()
        frame, arr, result = faceMask.DetectMask(frame)

        length += abs(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))

        if result == 'No mask':
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Sau khi anh dc lay tu camera n? se dc su dung ket hop voi file xml de cho ra gi? tri khu?n mat
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                if conf < 70:
                    profile = getProfile(Id)
                    ts = time.time()
                    timeStamp = datetime.datetime.fromtimestamp(
                        ts).strftime('%H:%M:%S')
                    date = datetime.datetime.fromtimestamp(
                        ts).strftime('%Y-%m-%d')
                    attendance.loc[len(attendance)] = [Id, date, timeStamp]
                    # Neu profile c? du lieu th? dua name v?o img
                    if profile != None:
                        cv2.putText(
                            frame, "" + str(profile[1]), (x + 5, y - 30), font, 0.5, (0, 255, 0), thickness=2)
                        # cv2.putText(
                        #     frame, "" + str(conf) + '%', (x + 5, y), font, 0.5, (0, 255, 0), thickness=2)
                    # googletts.speak(
                    #     f'Vui lòng đeo khẩu trang bạn {str(profile[1])}')
                    # time.sleep(5)
                else:
                    noOfFile = len(os.listdir(
                        "ImagesUnknown/"))+1
                    # messagebox.showwarning(
                    # "WARNING", "CÓ NGƯỜI LẠ!\nVUI LÒNG KIỂM TRA !!!")
                    cv2.putText(frame, "Unknown", (x, y + h + 30),
                                font, 0.4, (0, 0, 255), 1)
                    if length % 5 == 0:
                        cv2.imwrite(f"ImagesUnknown/Image_{length}" + str(noOfFile) +
                                    ".jpg", frame[y: y + h, x: x + w])
        attendance = attendance.drop_duplicates(
            subset=['Id'], keep='first')
        cv2.imshow('frame', frame)
        # ch = cv2.waitKey(20)
        if cv2.waitKey(1) == ord('q'):
            break

    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour, Minute, Second = timeStamp.split(":")

    fileName = "Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    attendance.to_csv(fileName, index=False)

    cap.release()
    cv2.destroyAllWindows()
    # print(attendance)
    res = attendance
    message2.configure(text=res)


def Update():
    # update to DB
    id = txt.get()
    name = txt2.get()
    role = txtRole.get()
    numPhone = txtNumberPhone.get()
    address = txtAddress.get()

    if (is_number(id) == False):
        messagebox.showwarning("WARNING", "VUI LÒNG NHẬP THÔNG TIN NHÂN VIÊN!")
    elif (is_number(id) == False):
        messagebox.showwarning("WARNING", "VUI LÒNG NHẬP ID LÀ MỘT SỐ!")
    elif (is_empty(name) != 0 or name.isspace()):
        messagebox.showwarning('WARNING', "VUI LÒNG NHẬP TÊN NHÂN VIÊN!")
    else:
        conn = sqlite3.connect(
            "data.db")
        query = "SELECT * FROM Employee WHERE ID = " + str(id)
        cursor = conn.execute(query)

        isRecordExist = 0

        for row in cursor:
            isRecordExist = 1

        if isRecordExist == 1:
            query = "UPDATE Employee SET Name = '" + str(name) + "', Role = '" + str(role) + "', NumberPhone = '" + str(
                numPhone) + "', Address = '" + str(address) + "' WHERE ID = " + str(id)
            conn.execute(query)
            conn.commit()
            conn.close()
            messagebox.showinfo("THÔNG BÁO", "CẬP NHẬT THÔNG TIN THÀNH CÔNG!")
        else:
            messagebox.showwarning(
                "WARNING", "NHÂN VIÊN NÀY KHÔNG ĐƯỢC LƯU TRỮ TRONG DANH SÁCH!!")


def Delete():
    id = txt.get()

    if (is_number(id) == False):
        messagebox.showwarning(
            "WARNING", "VUI LÒNG NHẬP ID CẦN XOÁ!")
    elif (is_number(id) == False):
        messagebox.showwarning("WARNING", "VUI LÒNG NHẬP ID LÀ MỘT SỐ!")
    else:
        # Delete from Database
        # delete(id, name, role, numPhone, address)
        conn = sqlite3.connect(
            "data.db")
        query = "SELECT * FROM Employee WHERE ID = " + str(id)
        cursor = conn.execute(query)

        isRecordExist = 0

        for row in cursor:
            isRecordExist = 1
        if isRecordExist == 1:
            # Delete in database
            query = "DELETE FROM Employee WHERE ID = " + str(id)
            conn.execute(query)
            conn.commit()
            conn.close()
            # Delete Image
            for i in range(1, 102):
                path = 'TrainingImage/Image_' + id + \
                    '/User.' + id + '.' + str(i) + '.jpg'
                os.remove(path)
            path1 = 'TrainingImage/Image_' + id
            os.rmdir(path1)
            # Delete TrainImages

            messagebox.showinfo("THÔNG BÁO", "XÓA THÀNH CÔNG!")
        else:
            messagebox.showwarning(
                "WARNING", "NHÂN VIÊN NÀY KHÔNG ĐƯỢC LƯU TRỮ TRONG DANH SÁCH!!")


clearButton = tk.Button(window, text="Xóa Text", command=clear, fg="white", bg="Gray",
                        width=20, height=2, activebackground="white", font=('times', 15, ' bold '))
clearButton.place(x=950, y=390)
trackImg = tk.Button(window, text="Nhận Diện", command=TrackImages, fg="steel blue",
                     bg="aquamarine1", width=16, height=3, activebackground="white", font=('times', 15, ' bold '))
trackImg.place(x=200, y=500)
addEmployee = tk.Button(window, text="Thêm User", command=Add, fg="steel blue",
                        bg="cadetblue1", width=16, height=3, activebackground="white", font=('times', 15, ' bold '))
addEmployee.place(x=435, y=500)
updateEmployee = tk.Button(window, text="Cập Nhật Thông Tin", command=Update, fg="steel blue",
                           bg="OliveDrab1", width=16, height=3, activebackground="white", font=('times', 15, ' bold '))
updateEmployee.place(x=670, y=500)
deleteEmployee = tk.Button(window, text="Xóa User", command=Delete, fg="steel blue",
                           bg="OliveDrab1", width=16, height=3, activebackground="white", font=('times', 15, ' bold '))
deleteEmployee.place(x=905, y=500)
quitWindow = tk.Button(window, text="Thoát", command=window.destroy, fg="steel blue",
                       bg="OliveDrab1", width=16, height=3, activebackground="white", font=('times', 15, ' bold '))
quitWindow.place(x=1140, y=500)

copyWrite = tk.Text(window, background=window.cget(
    "background"), borderwidth=0, font=('times', 30, 'italic bold underline'))
copyWrite.tag_configure("superscript", offset=10)
copyWrite.configure(state="disabled", fg="white")
copyWrite.pack(side="left")
copyWrite.place(x=800, y=750)

window.mainloop()
