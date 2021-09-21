from sqlalchemy import create_engine
engine = create_engine('sqlite:///database.db', echo=True)
connection = engine.connect()
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey,insert,update,delete,select,and_
metadata = MetaData()
sv = Table('sv',metadata,
            Column('id',String,primary_key=True),
            Column('name',String),
            Column('lop',String),
            Column('sdt',String))

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
def update_sinhvien(id,name=None,lop=None,sdt=None):
    if name == None:
        if lop == None and sdt == None:
            return False
        elif lop == None and sdt != None:
            update_sv = update(sv).value(sdt=sdt).where(sv.columns.id==id)
            lenh = connection.execute(update_sv)
            lenh.close()
            return True
        elif lop != None and sdt == None:
            update_sv = update(sv).value(lop=lop).where(sv.columns.id == id)
            lenh = connection.execute(update_sv)
            lenh.close()
            return True
        else:
            update_sv = update(sv).value(lop=lop,sdt=sdt).where(sv.columns.id == id)
            lenh = connection.execute(update_sv)
            lenh.close()
            return True
    else:
        if lop == None and sdt == None:
            update_sv = update(sv).value(name=name).where(sv.columns.id == id)
            lenh = connection.execute(update_sv)
            lenh.close()
            return True
        elif lop == None and sdt != None:
            update_sv = update(sv).value(sdt=sdt,name=name).where(sv.columns.id == id)
            lenh = connection.execute(update_sv)
            lenh.close()
        elif lop != None and sdt == None:
            update_sv = update(sv).value(lop=lop,name=name).where(sv.columns.id == id)
            lenh = connection.execute(update_sv)
            lenh.close()
            return True
        else:
            update_sv = update(sv).value(lop=lop, sdt=sdt,name=name).where(sv.columns.id == id)
            lenh = connection.execute(update_sv)
            lenh.close()
            return True

