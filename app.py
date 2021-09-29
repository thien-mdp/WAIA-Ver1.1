import tkinter as tk
from tkinter import ttk,messagebox
from PIL import ImageTk, Image
import cv2
from random import randrange
import os
from camera import MyVideoCapture
import test_train
from datetime import datetime
from threading import Thread
from database import get_so_lan_vi_pham,sv,engine,metadata,check_sinhvien,update_sinhvien,del_sinhvien,add_sinhvien,get_sinhhvien,del_all_sv,get_one_sv,get_ds_vi_pham,check_vi_pham_hop_le
import shutil
#Folder Dataset
FOLDER = "dataset/"
import time

def get_time():
    now = datetime.now()

    now = str(now).split(" ")
    key1 = "".join(now[0].split("-"))
    key2 = "".join(now[1].split(":")).split(".")[0]
    key = key1 + key2
    return key

class Login(tk.Tk):
    def __init__(self):
        super().__init__()
        self.logins = None
        self.geometry('350x500')
        self.title(' L O G I N ')
        self.resizable(0, 0)
        self.get__frame_login()
    def get__frame_login(self):
        j = 0
        r = 10
        for i in range(100):
            c = str(222222 + r)
            self.login = tk.Frame(self, width=10, height=500, bg="#" + c).place(x=j, y=0)
            j = j + 10
            r = r + 1
        self.login2 = tk.Frame(self,width=250,height=400,bg='white').place(x=50,y=50)
        self.l1 = tk.Label(self, text='Username', bg='white')
        l = ('Consolas', 13)
        self.l1.config(font=l)
        self.l1.place(x=80, y=200)

        # e1 entry for username entry
        self.e1 = tk.Entry(self, width=20, border=0)
        l = ('Consolas', 13)
        self.e1.config(font=l)
        self.e1.place(x=80, y=230)

        # e2 entry for password entry
        self.e2 = tk.Entry(self, width=20, border=0, show='*')
        self.e2.config(font=l)
        self.e2.place(x=80, y=310)

        self.l2 = tk.Label(self, text='Password', bg='white')
        l = ('Consolas', 13)
        self.l2.config(font=l)
        self.l2.place(x=80, y=280)
        ###lineframe on entry

        self.frame3 = tk.Frame(self, width=180, height=2, bg='#141414').place(x=80, y=332)
        self.frame4 = tk.Frame(self, width=180, height=2, bg='#141414').place(x=80, y=252)


        self.imagea = Image.open("log.PNG")
        self.imageb = ImageTk.PhotoImage(self.imagea)

        self.label1 = tk.Label(image=self.imageb,
                       border=0,
                       justify=tk.CENTER)

        self.label1.place(x=115, y=50)
        self.bttn(100, 375, 'L O G I N', 'white', '#994422')

    #     # Command
    def cmd(self):
        global app
        if self.e1.get() == 'admin' and self.e2.get() == 'admin':
            messagebox.showinfo("LOGIN SUCCESSFULLY", "         W E L C O M E        ")
            app.destroy()
            app = APPMAIN()
            app.mainloop()

        else:
            messagebox.showwarning("LOGIN FAILED", "        PLEASE TRY AGAIN        ")

        # Button_with hover effect
    def bttn(self,x, y, text, ecolor, lcolor):
        def on_entera(e):
            myButton1['background'] = ecolor  # ffcc66
            myButton1['foreground'] = lcolor  # 000d33

        def on_leavea(e):
            myButton1['background'] = lcolor
            myButton1['foreground'] = ecolor

        myButton1 = tk.Button(self, text=text,
                           width=20,
                           height=2,
                           fg=ecolor,
                           border=0,
                           bg=lcolor,
                           activeforeground=lcolor,
                           activebackground=ecolor,
                           command=self.cmd)

        myButton1.bind("<Enter>", on_entera)
        myButton1.bind("<Leave>", on_leavea)

        myButton1.place(x=x, y=y)





#ham check id == INT ??

def check_id(id):
    try:
        id = int(id)
        return True
    except:
        return False
#ham check sdt
def check_sdt(sdt):
    if len(sdt) < 10 or len(sdt) > 16:
        return False
    return True
def chuyen_man_hinh_add_sv():
    app2 = App()
    luong_add = Thread(target=app2.mainloop())
    luong_add.start()
    # global app
    # app.destroy()
    # app = App()
    # app.mainloop()


class APPMAIN(tk.Tk):
    def __init__(self):
        super().__init__()
        self.sv = None
        self.contacts = []
        self.title("HỆ THỐNG NHẮC NHỞ ĐEO KHẨU TRANG")
        self.geometry("1200x800")
        self.create_table_sv()

        self.create_find_sv()
        self.label_kq = None
        self.form_update = None
        self.create_frame_show_kq_detect()

    #ham update thong tin 1 sinh vien

    def update_one_sv(self):
        name = self.name_update_entry.get()
        lop = self.lop_update_entry.get()
        sdt = self.sdt_update_entry.get()
        update_sinhvien(self.id_find,name=name,lop=lop,sdt=sdt)
    def create_frame_show_kq_detect(self):
        self.show_kq_detect = ttk.Frame(self)
        self.label_kq_detect = ttk.Label(self.show_kq_detect, text="",font=('Helvetica', 16))
        self.label_kq_detect.grid(row=0, column=0)
        text_show = ""
        self.show_kqs = ttk.Label(self.show_kq_detect, text=text_show,font=('Helvetica', 12))
        self.show_kqs.grid(row=1, column=0)
        self.show_kq_detect.grid(row=4, column=0)
    def nhan_dien_khau_trang(self):
        luong_detect = Thread(target=self.detect_mask)

        luong_detect.start()
    #ham nhan dien
    def detect_mask(self):
        video_frame = MyVideoCapture()
        try:
            os.mkdir("vipham")
        except:
            pass
        while True:
            list_id, list_result, ret, frame = video_frame.get_frame_detect()
            cv2.imshow("CẢNH BÁO ĐEO KHẨU TRANG", frame)
            text_show = ""
            for i in range(len(list_id)):
                text_show = text_show + "ID: {0} =>> {1}\n".format(list_id[i],list_result[i])
                if list_result[i] == "No mask" or list_result[i] == "Wrong":
                    name_img = str(get_time())+".jpg"
                    check = check_vi_pham_hop_le(list_id[i],name_img=name_img)
                    if check:
                        cv2.imwrite("vipham/" + name_img, frame)
            self.show_kqs['text'] = text_show
            self.label_kq_detect['text'] = "DANH SÁCH NHẬN DIỆN"
            self.show_kq_detect.update()
            if cv2.waitKey(20) == 27:
                self.show_kq_detect.destroy()
                break
        cv2.destroyAllWindows()


    #ham hien noi dung update
    def show_form_update(self):
        self.form_update = ttk.Frame(self)
        self.thongtin_update_label = ttk.Label(self.form_update,text="SỬA THÔNG TIN CỦA #ID{0}".format(self.id_find),font=('Helvetica', 16))
        self.thongtin_update_label.grid(row=0,column=0)
        #name
        self.name_update_label = ttk.Label(self.form_update,text="Tên SV: ")
        self.name_update_label.grid(row=1,column=0,sticky=tk.W)
        self.name_update_entry = tk.StringVar()
        self.name_update_entry = ttk.Entry(self.form_update)
        self.name_update_entry.grid(row=1,column=0,sticky=tk.E,ipadx=50)

        #lop
        self.lop_update_label = ttk.Label(self.form_update, text="Lớp SV: ")
        self.lop_update_label.grid(row=2, column=0, sticky=tk.W)
        self.lop_update_entry = tk.StringVar()
        self.lop_update_entry = ttk.Entry(self.form_update)
        self.lop_update_entry.grid(row=2, column=0, sticky=tk.E, ipadx=50)
        #sdt
        self.sdt_update_label = ttk.Label(self.form_update, text="SDT SV: ")
        self.sdt_update_label.grid(row=3, column=0, sticky=tk.W)
        self.sdt_update_entry = tk.StringVar()
        self.sdt_update_entry = ttk.Entry(self.form_update)
        self.sdt_update_entry.grid(row=3, column=0, sticky=tk.E, ipadx=50)

        #button update
        self.button_update_one_sv = ttk.Button(self.form_update,text= "UPDATE",command=self.update_one_sv)
        self.button_update_one_sv.grid(row=4,column=0)
        self.form_update.grid(row=4, column=0, sticky=tk.W, padx=20)
    def train_after_del(self):
        if self.form_update != None:
            self.form_update.destroy()
        list_data = os.listdir(FOLDER)
        if len(list_data)==0:
            self.label_kq['text'] = "Đã xóa thành công sinh viên! Vui lòng Reload lại danh sách!"
            self.frame_show_kq.update()
            return False
        verbose = True
        tic = time.perf_counter()
        print("Training KNN classifier...")
        # Creates Classifier
        classifier = test_train.train(FOLDER, model_save_path="trained_knn_model.clf", verbose=verbose)
        print("Training complete!")
        self.label_kq['text'] = "Đã xóa thành công sinh viên! Vui lòng Reload lại danh sách!"
        self.frame_show_kq.update()
    #ham xoa 1 sinh vien
    def xoa_sinh_vien(self):
        check = messagebox.askquestion("NGUY HIỂM", "Bạn có muốn xóa sinh viên này!")
        if check == "yes":
            del_sinhvien(self.id_find)
            shutil.rmtree('dataset/'+str(self.id_find))
            luong_train_lai = Thread(target=self.train_after_del)
            luong_train_lai.start()
    #ham tim kiem sinh vien va show ket qua
    def find_sinh_vien(self):
        if self.form_update != None:
            self.form_update.destroy()
        self.id_find = self.id_find_entry.get()
        if check_id(self.id_find) == False:
            messagebox.showwarning(
                "WARNING", "ID BẮT BUỘC LÀ SỐ NGUYÊN!! BẠN ĐÃ NHẬP SAI ID!")
            return False
        self.frame_show_kq = ttk.Frame(self)
        self.sinhvien_da_co = get_one_sv(self.id_find)
        if self.label_kq != None:
            self.label_kq.destroy()
        if self.sinhvien_da_co == False:
            self.label_kq = ttk.Label(self.frame_show_kq,text="Sinh viên bạn tìm không có !",font=('Helvetica', 13))
            self.label_kq.grid(row = 0,column=0)
            self.frame_show_kq.grid(row=3, column=0)
            return False
        text_show = "ID : {0}\t Tên: {1}\t Lớp: {2}\t SDT: {3}\t".format(self.sinhvien_da_co[0],self.sinhvien_da_co[1],self.sinhvien_da_co[2],self.sinhvien_da_co[3])
        self.label_kq = ttk.Label(self.frame_show_kq, text=text_show,font=('Helvetica', 13))
        self.label_kq.grid(row=0, column=0,columnspan=2)
        self.button_xoa_one_sv = ttk.Button(self.frame_show_kq,text = "Xóa Sinh Viên",command = self.xoa_sinh_vien)
        self.button_xoa_one_sv.grid(row=1,column = 0)
        self.button_update_sv = ttk.Button(self.frame_show_kq,text = "Sửa Thông Tin",command=self.show_form_update)
        self.button_update_sv.grid(row=1,column = 1)
        self.frame_show_kq.grid(row=3,column=0)



    #tao khung tim kiem
    def create_find_sv(self):
        self.find_frame = ttk.Frame(self)
        self.label_find = ttk.Label(self.find_frame,text="Nhập ID để tìm sinh viên: ")
        self.label_find.grid(row=0,column=0)
        self.id_find_entry = tk.StringVar()
        self.id_find_entry = ttk.Entry(self.find_frame,width = 40)
        self.id_find_entry.grid(row = 0,column=1)
        self.button_find = ttk.Button(self.find_frame,text="Tìm Kiếm",command=self.find_sinh_vien)
        self.button_find.grid(row=0,column=2)
        self.find_frame.grid(row=2,column=0,pady = 30,padx = 50)

    # adding data to the treeview
    def create_table_sv(self):
        self.table = ttk.Frame(self)
        self.label_phanmem = ttk.Label(self.table, text="PHẦM MỀM NHẮC NHỞ ĐEO KHẨU TRANG", font=('Helvetica', 25))
        self.label_phanmem.grid(row=0, column=0, pady=50)
        self.danhsach_label = ttk.Label(self.table, text="#DANH SÁCH SINH VIÊN", font=('Helvetica', 18))
        self.danhsach_label.grid(row=1, column=0, pady=10)
        self.tree = ttk.Treeview(self.table, column=("#1", "#2", "#3","#4"), show='headings')
        # self.tree.column("#1", anchor=tk.CENTER)

        self.tree.heading("#1", text="ID")

        # self.tree.column("#2", anchor=tk.CENTER)

        self.tree.heading("#2", text="TÊN")

        # self.tree.column("#3", anchor=tk.CENTER)

        self.tree.heading("#3", text="LỚP")
        # self.tree.column("#4", anchor=tk.CENTER)

        self.tree.heading("#4", text="SỐ ĐIỆN THOẠI")
        self.rows = get_sinhhvien()
        for row in self.rows:
            self.tree.insert('', tk.END, values=[row[0],row[1],row[2],row[3]])

        # bind the select event
        def item_selected(event):
            for selected_item in self.tree.selection():
                # dictionary
                item = self.tree.item(selected_item)
                # list
                record = item['values']
                #
                text_title = "ID: {0} \n" \
                             "TÊN: {1}\n" \
                             "LỚP: {2}\n" \
                             "SDT {3}\n".format(str(record[0]),record[1],record[2],"0"+str(record[3]))
                messagebox.showinfo(title='Thông Tin Sinh Viên',
                         message=text_title)

        self.tree.bind('<<TreeviewSelect>>', item_selected)

        self.tree.grid(row=2, column=0, sticky='nsew',rowspan=5,columnspan=3)
        self.scrollbar = ttk.Scrollbar(self.table, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=2, column=4, sticky='ns',rowspan=4)
        self.button_add_sv = ttk.Button(self.table, text="THÊM SINH VIÊN", command=chuyen_man_hinh_add_sv)
        self.button_add_sv.grid(row=2, column=5,padx=100)
        self.button_update_ds = ttk.Button(self.table, text="RELOAD DANH SÁCH", command=self.updates)
        self.button_update_ds.grid(row=3, column=5, padx=100)
        self.button_update_ds = ttk.Button(self.table, text="XÓA TẤT CẢ SINH VIÊN", command=self.delete_all_sv)
        self.button_update_ds.grid(row=4, column=5, padx=100)
        self.button_nhandien = ttk.Button(self.table, text="BẮT ĐẦU NHẬN DIỆN", command=self.nhan_dien_khau_trang)
        self.button_nhandien.grid(row=5, column=5, padx=100)
        self.button_show_ds_vipham = ttk.Button(self.table,text="SHOW DANH SÁCH VI PHẠM",command=self.show_danh_sach_vi_pham)
        self.button_show_ds_vipham.grid(row=6, column=5, padx=100)
        self.table.grid(column=0, row=1,padx=50)
    def show_danh_sach_vi_pham(self):
        app2 = APPVIPHAM()
        app2.mainloop()
    def updates(self):
        self.rows = get_sinhhvien()
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in self.rows:
            self.tree.insert('', tk.END, values=[row[0], row[1], row[2], row[3]])
        self.table.update()
    def delete_all_sv(self):
        check = messagebox.askquestion("NGUY HIỂM","Bạn có muốn xóa toàn bộ sinh viên!")
        if check == 'yes':
            shutil.rmtree('dataset')
            os.mkdir(FOLDER)
            del_all_sv()





class App(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.frame = None
        self.create_video_frame()
        self.delay = 1
        self.geometry("1600x800")
        self.title("THÊM SINH VIÊN")
        self.list_anh_show = []
        self.num_img = 1
        self.check_anh_chup_dau = True
        self.get_image_temp = None
    def update(self):
        ret, self.frame,self.frame2 = self.video_frame.get_frame()
        if ret:
            self.photo2 = ImageTk.PhotoImage(image=Image.fromarray(self.frame2))
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.video.after(1,self.update)

    def update_detect(self):
        ret, self.frame = self.video_frame.get_frame_detect()
        if ret:
            self.photo2 = ImageTk.PhotoImage(image=Image.fromarray(self.frame2))
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.video.after(1,self.update_detect)
    def create_video_frame(self):
        self.video = ttk.Frame(self)
        self.video_frame = MyVideoCapture()
        self.id_label = ttk.Label(self.video,text="Nhập ID:")
        self.id_label.grid(row=0,column=0)
        self.id = tk.StringVar()
        self.id = ttk.Entry(self.video,width=30)
        self.id.grid(row=0,column=1)
        #nhap ten
        self.ten_label = ttk.Label(self.video,text="Nhập Tên:")
        self.ten_label.grid(row = 1,column = 0)
        self.ten = tk.StringVar()
        self.ten = ttk.Entry(self.video,width=30)
        self.ten.grid(row = 1,column = 1)
        #nhap chuc vu
        self.ten_lop_label = ttk.Label(self.video, text="Nhập Tên Lớp:")
        self.ten_lop_label.grid(row=2, column=0)
        self.ten_lop = tk.StringVar()
        self.ten_lop = ttk.Entry(self.video, width=30)
        self.ten_lop.grid(row=2, column=1)
        #nhap sdt
        self.sdt_label = ttk.Label(self.video, text="Nhập SDT:")
        self.sdt_label.grid(row=3, column=0)
        self.sdt = tk.StringVar()
        self.sdt = ttk.Entry(self.video, width=30)
        self.sdt.grid(row=3, column=1)
        #camera
        self.canvas = tk.Canvas(self.video,width=self.video_frame.width,height=self.video_frame.height)
        self.canvas.grid(row = 0, column = 2,rowspan=4,padx = 60)
        self.button_chup = ttk.Button(self.video,text="Chụp Ảnh ",command=self.chup_anh)
        self.button_chup.grid(row = 5,column=2,pady = 20)
        #button chuyen sang nhan dien
        self.button_nhan_dien = ttk.Button(self.video, text="Nhận Diện", command=nhan_dien_khau_trang)
        self.button_nhan_dien.grid(row=5, column=3, pady=20)
        # button them sinh vien
        self.showed_video = self.update()
        self.video.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)
    def chup_anh(self):
        try:
            os.mkdir('dataset')
        except:
            pass
        id = self.id.get()
        if self.get_image_temp != None and id != self.get_image_temp:
            self.check_anh_chup_dau = True
            for i in self.list_anh_show:
                i.destroy()
            self.list_anh_show = []
        if self.check_anh_chup_dau == True:
            try:
                shutil.rmtree("dataset/" + str(id))
            except:
                pass
        if check_id(id) == False:
            messagebox.showwarning(
                "WARNING", "ID BẮT BUỘC LÀ SỐ NGUYÊN!! BẠN ĐÃ NHẬP SAI ID!")
            return False
        self.id_sv = id
        try:
            os.mkdir(FOLDER+str(id))
        except:
            pass
        # name_img = FOLDER+str(id) +"img"+str(randrange(1000,10000))+".jpg"
        name_img = FOLDER+str(id)+"/"+"img"+str(randrange(1000,10000))+".jpg"
        imgpil = ImageTk.getimage(self.photo2)
        imgpil = imgpil.convert('RGB')
        imgpil.save(name_img,"JPEG")
        imgpil.close()
        print('ok')
        self.get_image_temp = id
        self.anh_da_chup_label = ttk.Label(self.video,text="Image FACE {0}/9: ".format(self.num_img))
        self.anh_da_chup_label.grid(row=0,column=3)
        self.button_clearn_img = ttk.Button(self.video,text = "Clear Img",command = self.clear_img)
        self.button_clearn_img.grid(row = 0 ,column = 4)
        self.list_img = os.listdir(FOLDER+str(id)+"/")
        for (index,img) in enumerate(self.list_img):
            self.show_list_image(FOLDER+str(id)+"/"+img,row=1+int(index/3),col=3+index%3)
        self.num_img = len(self.list_img) + 1
        if self.num_img == 10:
            self.button_chup["state"] = "disabled"
            self.button_them_sv = ttk.Button(self.video,text = "Thêm Sinh Viên",command = self.train)
            self.button_them_sv.grid(row = 6,column=1,pady = 10)
            self.check_anh_chup_dau = True
        self.check_anh_chup_dau = False
    def show_list_image(self,name_img,row,col):
        img = Image.open(name_img)
        image1 = img.resize((70, 70), Image.ANTIALIAS)
        image1 = ImageTk.PhotoImage(image1)
        self.anh_chup = ttk.Label(self.video, image=image1)
        self.anh_chup.grid(row=row, column=col)
        self.anh_chup.image = image1
        self.list_anh_show.append(self.anh_chup)
        # self.anh_da_chup_label = ttk.Label(self.video, text="Image FACE {0}/10: ".format(self.num_img))
    def clear_img(self):
        for i in self.list_anh_show:
            i.destroy()
        self.list_anh_show = []
        self.num_img = 1
        self.id.delete(0, 'end')
    def train_thread(self):
        #xu ly data truoc khi train
        #get all thu muc con cua thu muc dataset
        list_data_sv = get_sinhhvien()
        list_sv = []
        for sv in list_data_sv:
            list_sv.append(str(sv[0]))
        list_data = os.listdir('dataset')
        for data in list_data:
            if str(data) not in list_sv:
                shutil.rmtree('dataset/'+str(data))
        verbose = True
        tic = time.perf_counter()
        print("Training KNN classifier...")
        # Creates Classifier
        classifier = test_train.train(FOLDER, model_save_path="trained_knn_model.clf", verbose=verbose)
        print("Training complete!")
        toc = time.perf_counter()
        if verbose:
            text_result_train = f"THÊM THÀNH CÔNG !! Đã train nhận diện sinh viên trong {toc - tic:0.4f} giây"
            self.label_result_train = ttk.Label(self.video,text =text_result_train)
            self.label_result_train.grid(row = 6,column=2,pady = 20)
    def train(self):
        self.name_sv = self.ten.get()
        if self.name_sv == "":
            messagebox.showwarning(
                "WARNING", "CHƯA NHẬP TÊN SINH VIÊN!")
            return False
        self.lop_sv = self.ten_lop.get()
        if self.lop_sv == "":
            messagebox.showwarning(
                "WARNING", "CHƯA NHẬP LỚP CỦA SINH VIÊN!")
            return False
        self.sdt_sv = self.sdt.get()

        #có thể check số điện thoai nếu muốn
        if check_sdt(self.sdt_sv) == False:
            messagebox.showwarning(
                "WARNING", "CHƯA NHẬP HOẶC NHẬP SAI SDT CỦA SINH VIÊN!")
            return False
        result_add = add_sinhvien(self.id_sv,self.name_sv,self.lop_sv,self.sdt_sv)
        if result_add == False:
            messagebox.showwarning(
                "WARNING", "SINH VIÊN ĐÃ TỒN TẠI!!")
            return False
        luong_train = Thread(target=self.train_thread)
        luong_train.start()


def detect_mask():
    video_frame = MyVideoCapture()
    while True:
        list_name, list_result, ret, frame = video_frame.get_frame_detect()
        cv2.imshow("CẢNH BÁO ĐEO KHẨU TRANG", frame)
        if cv2.waitKey(24) == 27:
            break
    cv2.destroyAllWindows()

def nhan_dien_khau_trang():
    luong_detect = Thread(target=detect_mask)
    luong_detect.start()


class APPVIPHAM(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.frame = None
        self.create_table_vi_pham()
        self.geometry("1300x600")
    def create_table_vi_pham(self):
        self.table = ttk.Frame(self)
        self.label_phanmem = ttk.Label(self.table, text="DANH SÁCH VI PHẠM ĐEO KHẨU TRANG", font=('Helvetica', 25))
        self.label_phanmem.grid(row=0, column=0, pady=50)
        self.danhsach_label = ttk.Label(self.table, text="#DANH SÁCH SINH VIÊN VI PHẠM", font=('Helvetica', 18))
        self.danhsach_label.grid(row=1, column=0, pady=10)
        self.tree = ttk.Treeview(self.table, column=("#1", "#2", "#3", "#4","#5","#6"), show='headings')
        # self.tree.column("#1", anchor=tk.CENTER)

        self.tree.heading("#1", text="ID")

        # self.tree.column("#2", anchor=tk.CENTER)

        self.tree.heading("#2", text="TÊN")

        # self.tree.column("#3", anchor=tk.CENTER)

        self.tree.heading("#3", text="LỚP")
        # self.tree.column("#4", anchor=tk.CENTER)

        self.tree.heading("#4", text="SỐ ĐIỆN THOẠI")
        self.tree.heading("#5", text="THỜI GIAN VI PHẠM")
        self.tree.heading("#6", text="PATH ẢNH VI PHẠM")
        self.rows = get_ds_vi_pham()
        for row in self.rows:
            self.tree.insert('', tk.END, values=[row[0], row[1], row[2], row[3],row[4],row[5]])

        # bind the select event
        def item_selected(event):
            for selected_item in self.tree.selection():
                # dictionary
                item = self.tree.item(selected_item)
                # list
                record = item['values']
                so_lan = get_so_lan_vi_pham(str(record[0]))
                #
                text_title = "ID: {0} \n" \
                             "TÊN: {1}\n" \
                             "LỚP: {2}\n" \
                             "SDT: {3}\n" \
                             "LẦN CUỐI VI PHẠM VÀO THỜI GIAN: {4}\n" \
                             "SỐ LẦN VI PHẠM: {5}".format(str(record[0]), record[1], record[2], "0" + str(record[3]),str(record[4]),so_lan)
                messagebox.showinfo(title='Thông Tin Sinh Viên Vi Phạm',
                                    message=text_title)

        self.tree.bind('<<TreeviewSelect>>', item_selected)

        self.tree.grid(row=2, column=0, sticky='nsew', rowspan=4, columnspan=3)
        self.scrollbar = ttk.Scrollbar(self.table, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=2, column=4, sticky='ns', rowspan=4)
        self.button_update_ds = ttk.Button(self.table, text="RELOAD DANH SÁCH VI PHẠM", command=self.updates)
        self.button_update_ds.grid(row=6, column=0, padx=50,pady = 30)
        self.table.grid(column=0, row=1, padx=50)

    def updates(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.rows = get_ds_vi_pham()
        for row in self.rows:
            self.tree.insert('', tk.END, values=[row[0], row[1], row[2], row[3], row[4], row[5]])
        self.table.update()

if __name__ == '__main__':
    metadata.create_all(engine)
    app = APPMAIN()
    app.mainloop()
