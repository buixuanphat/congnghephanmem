from app.models import NhanVien, GiaoVienChuNhiem, HocKy, HocSinh, KhoiLop, PhongHoc, KhoiPhong, DanhSachLop
from app import app
import  hashlib

def auth_user(taikhoan, matkhau):
    matkhau = str(hashlib.md5(matkhau.strip().encode('utf-8')).hexdigest())

    return NhanVien.query.filter(NhanVien.taiKhoan.__eq__(taikhoan),
                                 NhanVien.matKhau.__eq__(matkhau)).first()


def get_nhan_vien_by_id(id):
    return NhanVien.query.get(id)


def get_nhan_vien_by_role(role):
    return NhanVien.query.filter(NhanVien.vaiTro.__eq__(role))
