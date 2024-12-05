import hashlib

from flask import redirect, flash
from flask_admin import Admin, BaseView, expose
from app import app, db
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from app.models import NhanVien, HocSinh, DanhSachLop, GiaoVienChuNhiem, MonHoc, GiaoVien, UserRole, PhongHoc, KhoiPhong

admin = Admin(app=app, name='Người Quản Trị', template_mode='bootstrap4')



class DanhSachLopView(ModelView):
    pass

class GiaoVienView(ModelView):
    form_columns = ['hoTen', 'gioiTinh', 'ngaySinh', 'diaChi', 'SDT', 'eMail', 'taiKhoan', 'matKhau', 'monHoc']

    def on_model_change(self, form, model, is_created):
        if form.matKhau.data:
            model.matKhau = hashlib.md5(form.matKhau.data.encode('utf-8')).hexdigest()

        super(GiaoVienView, self).on_model_change(form, model, is_created)

class KhoiPhongView(ModelView):
    column_list = ['id', 'KhoiLop', 'PhongHoc', 'buoiHoc']
    form_columns = ['KhoiLop', 'PhongHoc', 'buoiHoc']


    # def on_model_change(self, form, model, is_created):
    #     dsKhoiPhong = KhoiPhong.query.all()
    #     for khoiphong in dsKhoiPhong:
    #         if(form.KhoiLop.data.__eq__(khoiphong.KhoiLop) and form.PhongHoc.data.__eq__(khoiphong.PhongHoc)
    #             and form.buoiHoc.data.__eq__(khoiphong.buoiHoc)):
    #             flash("Khối phòng đó đã được tạo", "error")
    #             is_created==False
    #             return redirect('/admin/khoiphong/new')
    #
    #     super(GiaoVienView, self).on_model_change(form, model, is_created)
    #
    # def on



admin.add_view(ModelView(MonHoc, db.session))
admin.add_view(ModelView(PhongHoc, db.session))
admin.add_view(KhoiPhongView(KhoiPhong, db.session))
admin.add_view(ModelView(NhanVien, db.session))
admin.add_view(GiaoVienView(GiaoVien, db.session))
admin.add_view(ModelView(GiaoVienChuNhiem, db.session))
admin.add_view(ModelView(HocSinh, db.session))
admin.add_view(DanhSachLopView(DanhSachLop, db.session))

