from flask_admin import Admin
from flask import redirect, url_for, flash
from flask_admin.actions import action
from app import app, db
from flask_admin.contrib.sqla import ModelView
from app.models import NhanVien, HocSinh, DanhSachLop

admin = Admin(app=app, name='Người Quản Trị', template_mode='bootstrap4')


class DanhSachLopView(ModelView):
    pass






admin.add_view(ModelView(NhanVien, db.session))
admin.add_view(ModelView(HocSinh, db.session))
admin.add_view(DanhSachLopView(DanhSachLop, db.session))

