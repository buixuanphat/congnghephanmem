from datetime import date
from enum import unique

from app import db, app
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, BOOLEAN, Date
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

class NhanVien(db.Model):
    idNhanVien = Column(Integer, primary_key=True, autoincrement=True)
    hoTen = Column(String(50),nullable=False)
    gioiTinh = Column(Boolean,nullable=False)
    ngaySinh = Column(Date,nullable=False)
    diaChi = Column(String(255),nullable=False)
    SDT = Column(String(20), unique=True,nullable=False)
    eMail = Column(String(255), unique=True,nullable=False)
    taiKhoan = Column(String(50), unique=True, nullable=False)
    matKhau = Column(String(255), nullable=False)

    def __str__(self):
        return self.hoTen

    def set_password(self, password):
        self.matKhau = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.matKhau,password)


class HocSinh(db.Model):
    idHocSinh = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hoTen = db.Column(db.String(50), nullable=False)
    gioiTinh = db.Column(db.Boolean, nullable=False)
    ngaySinh = db.Column(db.Date, nullable=False)
    diaChi = db.Column(db.String(255), nullable=False)
    SDT = db.Column(db.String(20), unique=True, nullable=False)
    eMail = db.Column(db.String(255), unique=True, nullable=False)


class KhoiLop(db.Model):
    idKhoiLop = Column(Integer, primary_key=True, autoincrement=True)
    tenKhoi = Column(String(10), unique=True, nullable=False)

    # Quan hệ Nhiều-Nhiều với PhongHoc
    phong_hocs = db.relationship('PhongHoc', secondary='khoi_phong', back_populates='khoi_lops')

    def __str__(self):
        return self.tenKhoi

class PhongHoc(db.Model):
    idPhongHoc = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tenPhong = db.Column(db.String(50), unique=True, nullable=False)  # VD: "Phòng 101", "Phòng 202"

    # Quan hệ Nhiều-Nhiều với KhoiLop
    khoi_lops = db.relationship('KhoiLop', secondary='khoi_phong', back_populates='phong_hocs')

    def __str__(self):
        return self.tenPhong

# Bảng trung gian giữa KhoiLop và PhongHoc
class KhoiPhong(db.Model):
    __tablename__ = 'khoi_phong'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    khoiLop_id = db.Column(db.Integer, db.ForeignKey('khoi_lop.idKhoiLop'), nullable=False)
    phongHoc_id = db.Column(db.Integer, db.ForeignKey('phong_hoc.idPhongHoc'), nullable=False)

if __name__== '__main__':
    with app.app_context():
        db.create_all()

        # kh1 = KhoiLop(tenKhoi="10")
        # kh2 = KhoiLop(tenKhoi="11")
        # kh3 = KhoiLop(tenKhoi="12")
        #
        # ph1 = PhongHoc(tenPhong="Phòng 101")
        # ph2 = PhongHoc(tenPhong="Phòng 102")
        # ph3 = PhongHoc(tenPhong="Phòng 201")
        #
        # # Liên kết phòng học với các khối lớp
        # ph1.khoi_lops.extend([kh1, kh2])  # Phòng 101 được sử dụng bởi khối 10 và khối 11
        # ph2.khoi_lops.append(kh1)  # Phòng 102 được sử dụng bởi khối 10
        # ph3.khoi_lops.append(kh3)  # Phòng 201 được sử dụng bởi khối 12
        #
        # db.session.add_all([kh1, kh2, kh3, ph1, ph2, ph3])
        # db.session.commit()

        # nv = NhanVien(
        #     hoTen="Tô Quốc Bình",
        #     gioiTinh=True,
        #     ngaySinh=date(2004, 2, 21),
        #     diaChi="Thành phố Hồ Chí Minh",
        #     SDT="0762590966",
        #     eMail="toquocbinh2102@gmail.com",
        #     taiKhoan="quocbinh"
        # )
        # nv.set_password("123456")
        # db.session.add(nv)
        # db.session.commit()

