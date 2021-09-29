from sqlalchemy import create_engine
from datetime import datetime,timedelta
engine = create_engine('sqlite:///database.db?check_same_thread=False', echo=True)
connection = engine.connect()
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey,insert,update,delete,select,and_,DateTime
metadata = MetaData()
sv = Table('sv',metadata,
            Column('id',String,primary_key=True),
            Column('name',String),
            Column('lop',String),
            Column('sdt',String))
vipham = Table('vipham',metadata,
            Column('id',String),
            Column('name',String),
            Column('lop',String),
            Column('sdt',String),
            Column('thoigian',DateTime,default=datetime.now()),
            Column("path_img",String))

def get_so_lan_vi_pham(id):
    check = select([vipham]).where(vipham.columns.id == id)
    lenh = connection.execute(check)
    so_lan = len(lenh.fetchall())
    lenh.close()
    return so_lan

def del_all_vipham():
    del_all = delete(vipham)
    lenh = connection.execute(del_all)
    lenh.close()
def check_vi_pham_hop_le(id,name_img):
    check = select([vipham]).where(vipham.columns.thoigian >= datetime.now()-timedelta(days=0,minutes=3))
    lenh = connection.execute(check)
    list_vipham_two_min = lenh.fetchall()
    lenh.close()
    if len(list_vipham_two_min) == 0:
        add_vipham(id,name_img)
        return True
    list_id = []
    for sv in list_vipham_two_min:
        list_id.append(sv[0])
    print(list_id)
    if str(id) in list_id:
        print("tessttttt")
        return False
    add_vipham(id, name_img)
    return True
def get_ds_vi_pham():
    get_all_vipham = select([vipham])
    lenh = connection.execute(get_all_vipham)
    list_vipham = lenh.fetchall()
    lenh.close()
    return list_vipham
def add_vipham(id,name_img):
    get_one = select([sv]).where(sv.columns.id == id)
    lenh = connection.execute(get_one)
    sinhviens = lenh.fetchall()
    lenh.close()
    if len(sinhviens) == 0:
        return False
    sinhvien = sinhviens[0]
    name_img = "vipham/"+name_img
    add = insert(vipham).values(id=id,name=sinhvien[1],lop=sinhvien[2],sdt=sinhvien[3],path_img = name_img)
    lenh = connection.execute(add)
    lenh.close()
    return True


def get_one_sv(id):
    get_one = select([sv]).where(sv.columns.id==id)
    lenh = connection.execute(get_one)
    sinhvien = lenh.fetchall()
    if len(sinhvien) == 0:
        return False
    return sinhvien[0]
def del_all_sv():
    del_all = delete(sv)
    lenh = connection.execute(del_all)
    lenh.close()

def get_sinhhvien():
    get_sv = select([sv])
    lenh = connection.execute(get_sv)
    sinhvien = lenh.fetchall()
    lenh.close()
    return sinhvien
def check_sinhvien(id):
    check_sv = select([sv]).where(sv.columns.id==id)
    lenh = connection.execute(check_sv)
    sinhvien_tontai = lenh.fetchall()
    lenh.close()
    if len(sinhvien_tontai) == 0:
        return False
    return True

def add_sinhvien(id,name,lop,sdt):
    if check_sinhvien(id) == True:
        return False
    new_sv = insert(sv).values(id=id,name=name,lop=lop,sdt=sdt)
    lenh = connection.execute(new_sv)
    lenh.close()
    return True
def del_sinhvien(id):
    tim_sv = delete(sv).where(sv.columns.id ==id)
    lenh = connection.execute(tim_sv)
    lenh.close()
def update_sinhvien(id,name="",lop="",sdt=""):
    if name == "":
        if lop == "" and sdt == "":
            return False
        elif lop == "" and sdt != "":
            update_sv = update(sv).values(sdt=sdt).where(sv.columns.id==id)
            lenh = connection.execute(update_sv)
            lenh.close()
            return True
        elif lop != "" and sdt == "":
            update_sv = update(sv).values(lop=lop).where(sv.columns.id == id)
            lenh = connection.execute(update_sv)
            lenh.close()
            return True
        else:
            update_sv = update(sv).values(lop=lop,sdt=sdt).where(sv.columns.id == id)
            lenh = connection.execute(update_sv)
            lenh.close()
            return True
    else:
        if lop == "" and sdt == "":
            update_sv = update(sv).values(name=name).where(sv.columns.id == id)
            lenh = connection.execute(update_sv)
            lenh.close()
            return True
        elif lop == "" and sdt != "":
            update_sv = update(sv).values(sdt=sdt,name=name).where(sv.columns.id == id)
            lenh = connection.execute(update_sv)
            lenh.close()
        elif lop != "" and sdt == "":
            update_sv = update(sv).values(lop=lop,name=name).where(sv.columns.id == id)
            lenh = connection.execute(update_sv)
            lenh.close()
            return True
        else:
            update_sv = update(sv).values(lop=lop, sdt=sdt,name=name).where(sv.columns.id == id)
            lenh = connection.execute(update_sv)
            lenh.close()
            return True

