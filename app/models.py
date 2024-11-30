from datetime import date

from app import db, app
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, BOOLEAN, Date, Enum
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum as RoleEnum
from flask_login import UserMixin
from sqlalchemy.orm import relationship

class UserRole(RoleEnum):
    ADMIN = 1
    NHANVIENTIEPNHAN = 2
    GIAOVIEN = 3
    NGUOIQUANTRI = 4

class NhanVien(db.Model, UserMixin):
    idNhanVien = Column(Integer, primary_key=True, autoincrement=True)
    hoTen = Column(String(50),nullable=False)
    gioiTinh = Column(Boolean,nullable=False)
    ngaySinh = Column(Date,nullable=False)
    diaChi = Column(String(255),nullable=False)
    SDT = Column(String(20), unique=True,nullable=False)
    eMail = Column(String(255), unique=True,nullable=False)
    vaiTro = Column(Enum(UserRole))
    taiKhoan = Column(String(50), unique=True, nullable=False)
    matKhau = Column(String(255), nullable=False)

    def __str__(self):
        return self.hoTen

    def set_password(self, password):
        self.matKhau = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.matKhau,password)

    def get_VaiTro(self):
        return self.vaiTro


class GiaoVienChuNhiem(NhanVien):
    __tablename__ = 'giao_vien_chu_nhiem'
    idNhanVien = Column(Integer, ForeignKey(NhanVien.idNhanVien), primary_key=True)
    idDsLop = Column(Integer, ForeignKey('danh_sach_lop.maDsLop'), nullable=True)

    # Quan hệ với DanhSachLop
    lopChuNhiem = relationship('DanhSachLop', backref='giaoVien')

    def __str__(self):
        return f"GV: {self.hoTen} - Lớp: {self.lopChuNhiem.tenLop if self.lopChuNhiem else 'Chưa phân lớp'}"


class HocKy(db.Model):
    idHocKy = Column(Integer, primary_key=True, autoincrement=True)
    namHoc = Column(String(20), nullable=False)
    hocKy = Column(String(20), nullable=False)

    def __str__(self):
        return f"{self.namHoc} - {self.hocKy}"

    def get_HocKy(self):
        return self.hocKy

    def get_NamHoc(self):
        return self.namHoc


class HocSinh(db.Model):
    idHocSinh = Column(Integer, primary_key=True, autoincrement=True)
    hoTen = Column(String(50), nullable=False)
    gioiTinh = Column(Boolean, nullable=False)
    ngaySinh = Column(Date, nullable=False)
    diaChi = Column(String(255), nullable=False)
    SDT = Column(String(20), unique=True, nullable=False)
    eMail = Column(String(255), unique=True, nullable=False)
    maDsLop = Column(Integer, ForeignKey('danh_sach_lop.maDsLop'), nullable=True)


class KhoiLop(db.Model):
    idKhoiLop = Column(Integer, primary_key=True, autoincrement=True)
    tenKhoi = Column(String(10), unique=True, nullable=False)

    # Quan hệ Nhiều-Nhiều với PhongHoc
    phong_hocs = db.relationship('PhongHoc', secondary='khoi_phong', back_populates='khoi_lops')

    def __str__(self):
        return self.tenKhoi


class PhongHoc(db.Model):
    idPhongHoc = Column(Integer, primary_key=True, autoincrement=True)
    tenPhong = Column(String(50), unique=True, nullable=False)  # VD: "Phòng 101", "Phòng 202"

    # Quan hệ Nhiều-Nhiều với KhoiLop
    khoi_lops = relationship('KhoiLop', secondary='khoi_phong', back_populates='phong_hocs')

    def __str__(self):
        return self.tenPhong

# Bảng trung gian giữa KhoiLop và PhongHoc
class KhoiPhong(db.Model):
    __tablename__ = 'khoi_phong'
    id = Column(Integer, primary_key=True, autoincrement=True)
    khoiLop_id = Column(Integer, ForeignKey('khoi_lop.idKhoiLop'), nullable=False)
    phongHoc_id = Column(Integer, ForeignKey('phong_hoc.idPhongHoc'), nullable=False)


class DanhSachLop(db.Model):
    maDsLop = Column(Integer, primary_key=True, autoincrement=True)
    tenPhong_id = Column(Integer, ForeignKey(PhongHoc.idPhongHoc), nullable=False)
    giaoVienChuNhiem_id = Column(Integer, ForeignKey(NhanVien.idNhanVien), nullable=True)
    siSo = db.Column(Integer, nullable=False)
    hocKy_id = Column(Integer, ForeignKey(HocKy.idHocKy), nullable=False)

    giaoVienChuNhiem = relationship('NhanVien', backref='lop')
    hocKy = relationship(HocKy, backref='lop')
    hocSinhs = relationship('HocSinh', backref='lop', lazy=True)

    def __str__(self):
        return f"{self.tenLop}"

if __name__== '__main__':
    with app.app_context():
        db.create_all()

        # hk1 = HocKy(namHoc="2024-2025", hocKy="1")
        # hk2 = HocKy(namHoc="2024-2025", hocKy="2")
        # db.session.add_all([hk1,hk2])
        # db.session.commit()

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


        # Tạo nhân viên

        # nv = NhanVien(
        #     hoTen="Tô Quốc Bình",
        #     gioiTinh=True,
        #     ngaySinh=date(2004, 2, 21),
        #     diaChi="Thành phố Hồ Chí Minh",
        #     SDT="0762590966",
        #     eMail="toquocbinh2102@gmail.com",
        #     vaiTro=UserRole.NHANVIENTIEPNHAN,
        #     taiKhoan="quocbinh"
        # )
        # nv.set_password("123456")
        # db.session.add(nv)
        # db.session.commit()

