from datetime import date
from email.policy import default

from app import db, app
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, BOOLEAN, Date, Enum, UniqueConstraint
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum as RoleEnum, unique
from flask_login import UserMixin
import hashlib
from sqlalchemy.orm import relationship, Relationship


class UserRole(RoleEnum):
    NGUOIQUANTRI = 1
    NHANVIENTIEPNHAN = 2

class Khoi(RoleEnum):
    KHOI10 = 1
    KHOI11 = 2
    KHOI12 = 3

class MonHoc(db.Model):
    idMonHoc = Column(Integer, primary_key=True, autoincrement=True)
    tenMonHoc = Column(String(50), nullable=False)
    giaoViens = relationship('GiaoVien',backref='monhoc', lazy=True)

    def __str__(self):
        return self.tenMonHoc

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

    # Thêm phương thức get_id nếu không dùng UserMixin
    def get_id(self):
        return str(self.idNhanVien)

    def set_password(self, password):
        self.matKhau = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.matKhau,password)

    def get_VaiTro(self):
        return self.vaiTro


class GiaoVien(db.Model):
    idGiaoVien = Column(Integer, primary_key=True)
    hoTen = Column(String(50), nullable=False)
    gioiTinh = Column(Boolean, nullable=False)
    ngaySinh = Column(Date, nullable=False)
    diaChi = Column(String(255), nullable=False)
    SDT = Column(String(20), unique=True, nullable=False)
    eMail = Column(String(255), unique=True, nullable=False)
    taiKhoan = Column(String(50), unique=True, nullable=False)
    matKhau = Column(String(255), nullable=False)
    idMonHoc = Column(Integer, ForeignKey(MonHoc.idMonHoc),nullable=False)

    monHoc = relationship(MonHoc,backref='giaovien')

    def __str__(self):
        return self.hoTen

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.idGiaoVien)


class GiaoVienDayHoc(db.Model):
    __tablename__ = 'giao_vien_day_hoc'
    idGiaoVienDayHoc = Column(Integer, primary_key=True,autoincrement=True)
    idGiaoVien = Column(Integer, ForeignKey(GiaoVien.idGiaoVien),nullable=True)
    idDsLop = Column(Integer, ForeignKey('danh_sach_lop.maDsLop', ondelete="CASCADE"), nullable=True)

    # Quan hệ với DanhSachLop
    giaoVien = relationship(GiaoVien, backref="dayLop")
    lopDay = relationship('DanhSachLop', backref='giaoVienPhuTrach')



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
    khoi = Column(String(50), nullable=False)
    diaChi = Column(String(255), nullable=False)
    SDT = Column(String(20), unique=True, nullable=False)
    eMail = Column(String(255), unique=True, nullable=False)
    maDsLop = Column(Integer, ForeignKey('danh_sach_lop.maDsLop'), nullable=True)

    hocSinhLop = relationship('DanhSachLop', backref='danhSachHocSinh')

class PhongHoc(db.Model):
    idPhongHoc = Column(Integer, primary_key=True, autoincrement=True)
    tenPhong = Column(String(50), unique=True, nullable=False)  # VD: "Phòng 101", "Phòng 202"

    def __str__(self):
        return self.tenPhong


class DanhSachLop(db.Model):

    maDsLop = Column(Integer, primary_key=True, autoincrement=True)
    idPhongHoc = Column(Integer, ForeignKey(PhongHoc.idPhongHoc),unique=True, nullable=True)
    tenLop = Column(String(50),unique=True,nullable=True)
    khoi = Column(String(50), nullable=False)
    giaoVienChuNhiem_id = Column(Integer, ForeignKey(GiaoVien.idGiaoVien), nullable=True)
    siSoHienTai = db.Column(Integer, nullable=False)
    siSo = db.Column(Integer, nullable=False)
    hocKy_id = Column(Integer, ForeignKey(HocKy.idHocKy), nullable=False)
    active = Column(Boolean, default=True)

    giaoVienChuNhiem = relationship(GiaoVien, backref='lop')
    hocKy = relationship(HocKy, backref='lop')
    hocSinhs = relationship(HocSinh, backref='danhSachLop', lazy=True)
    phongHoc = relationship(PhongHoc, backref='danhSachLops')

    # Thêm quan hệ với GiaoVienChuNhiem
    giaoVienDayHocs = relationship(
        'GiaoVienDayHoc',
        backref='lop',
        cascade="all, delete",
        lazy=True
    )

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
        #     hoTen="Trần Quốc Phong",
        #     gioiTinh=True,
        #     ngaySinh=date(2004, 10, 30),
        #     diaChi="Thành phố Hồ Chí Minh",
        #     SDT="0799773010",
        #     eMail="toquocphong2102@gmail.com",
        #     vaiTro=UserRole.NGUOIQUANTRI,
        #     taiKhoan="quocphong",
        #     matKhau=str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        # )
        # db.session.add(nv)
        # db.session.commit()

