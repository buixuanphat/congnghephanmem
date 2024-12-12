from app.models import NhanVien, GiaoVien, GiaoVienDayHoc, HocKy, HocSinh, PhongHoc, DanhSachLop
from app import app
import  hashlib

def auth_user(taikhoan, matkhau):
    matkhau = str(hashlib.md5(matkhau.strip().encode('utf-8')).hexdigest())

    return NhanVien.query.filter(NhanVien.taiKhoan.__eq__(taikhoan),
                                 NhanVien.matKhau.__eq__(matkhau)).first()

def auth_giao_vien(taikhoan, matkhau):
    matkhau = str(hashlib.md5(matkhau.strip().encode('utf-8')).hexdigest())

    # return GiaoVien.query.filter(GiaoVien.taiKhoan.__eq__(taikhoan),
    #                              GiaoVien.matKhau.__eq__(matkhau)).first()
    gv = GiaoVien.query.filter(GiaoVien.taiKhoan.__eq__(taikhoan),
                               GiaoVien.matKhau.__eq__(matkhau)).first()
    if gv:
        print(f"auth_giao_vien -> Tài khoản: {taikhoan}, Mật khẩu: {matkhau}, Kết quả: {gv}")
        return gv
    return None

def get_nhan_vien_by_id(id):
    return NhanVien.query.get(id)


def get_nhan_vien_by_role(role):
    return NhanVien.query.filter(NhanVien.vaiTro.__eq__(role))

def get_giao_vien_by_id(id):
    return GiaoVien.query.get(id)
