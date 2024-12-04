from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
from sqlalchemy import Nullable
from sqlalchemy.testing.plugin.plugin_base import config

from app import app, db, dao, login
from datetime import date,datetime
from app.models import NhanVien, HocSinh, UserRole, DanhSachLop, PhongHoc, HocKy, GiaoVienChuNhiem
from flask_login import login_user, logout_user

app.secret_key = 'secret_key'  # Khóa bảo mật cho session

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login_process():
    err_msg=None
    if request.method == 'POST':
        taiKhoan = request.form['taiKhoan']
        matKhau = request.form['matKhau']

        nv = dao.auth_user(taikhoan=taiKhoan,matkhau=matKhau)
        if nv and nv.get_VaiTro()==UserRole.NHANVIENTIEPNHAN:
            login_user(nv)
            return redirect('/nhan-vien-tiep-nhan')
        elif nv and nv.get_VaiTro()==UserRole.NGUOIQUANTRI:
            login_user(nv)
            return redirect('/admin')
        else:
            err_msg = "Sai tài khoản/ mật khẩu"
    return render_template('layout/login.html', err_msg=err_msg)



@app.route('/nhan-vien-tiep-nhan')
def dashboard():
    return render_template('layout/nhanvientiepnhan.html')

@app.route('/logout', methods=['get', 'post'])
def logout_process():
    logout_user()
    return redirect('/login')

@login.user_loader
def load_user(user_id):
    return dao.get_nhan_vien_by_id(user_id)

# @app.before_request
# def require_login():
#     allowed_routes = ['login', 'logout']
#     if request.endpoint not in allowed_routes and not session.get('logged_in'):
#         return redirect('/login')

@app.route('/nhap-ho-so', methods=['POST'])
def kiem_tra_tuoi():

    ngay_sinh = request.form.get('ngaySinh')
    if ngay_sinh:
        # Tính tuổi
        ngay_sinh = datetime.strptime(ngay_sinh, "%Y-%m-%d").date()
        hom_nay = date.today()
        tuoi = hom_nay.year - ngay_sinh.year - ((hom_nay.month, hom_nay.day) < (ngay_sinh.month, ngay_sinh.day))

        # Kiểm tra tuổi
        if app.config["MIN_AGE"] <= tuoi <= app.config["MAX_AGE"]:
            flash("Tuổi hợp lệ. Hãy nhập thông tin chi tiết.", "success")
            return render_template('layout/nhap_thong_tin_hoc_sinh.html', ngay_sinh=ngay_sinh)
        else:
            flash(f"Tuổi không phù hợp: {tuoi} tuổi!!!", "warning")
            return redirect('/nhan-vien-tiep-nhan')
    return "Không nhận được thông tin ngày sinh!"

@app.route('/luu-hoc-sinh', methods=['POST'])
def luu_hoc_sinh():

    # Lấy thông tin từ form
    ho_ten = request.form.get('hoTen')
    gioi_tinh = request.form.get('gioiTinh')  # Nam = 1, Nữ = 0
    ngay_sinh = request.form.get('ngaySinh')
    dia_chi = request.form.get('diaChi')
    so_dien_thoai = request.form.get('soDienThoai')
    email = request.form.get('email')

    # Tạo đối tượng học sinh mới
    hoc_sinh = HocSinh(
        hoTen=ho_ten,
        gioiTinh=(gioi_tinh == '1'),
        ngaySinh=datetime.strptime(ngay_sinh, "%Y-%m-%d").date(),
        diaChi=dia_chi,
        SDT=so_dien_thoai,
        eMail=email,
        maDsLop = None
    )
    db.session.add(hoc_sinh)
    db.session.commit()

    flash("Học sinh đã được lưu thành công!", "success")
    return redirect("/nhan-vien-tiep-nhan")

@app.route('/tao-danh-sach-lop')
def create_auto_classes():
    try:
        # Lấy toàn bộ danh sách học sinh
        students = HocSinh.query.filter(HocSinh.maDsLop == None).all()
        if not students:
            flash("Không có học sinh nào để tạo lớp!", "error")
            return redirect('/admin')

         # Tạo một lớp mới
        phong_hoc = PhongHoc.query.first()  # Giả định có sẵn một phòng học
        hoc_ky = HocKy.query.first()  # Giả định có sẵn một học kỳ
        if not phong_hoc or not hoc_ky:
            return jsonify({"error": "Phòng học hoặc học kỳ không tồn tại"}), 400



        batch_size = 4  # Số học sinh mỗi lớp
        for i in range(0, len(students), batch_size):
            class_students = students[i:i + batch_size]

            # Tạo danh sách lớp mới
            new_class = DanhSachLop(
                tenPhong_id=phong_hoc.idPhongHoc,  # Thay đổi nếu cần
                giaoVienChuNhiem_id=None,
                siSo=len(class_students),
                hocKy_id=1  # Đặt ID học kỳ phù hợp
            )
            db.session.add(new_class)
            db.session.commit()

            # Gán học sinh vào lớp
            for student in class_students:
                student.maDsLop = new_class.maDsLop
                db.session.add(student)

        db.session.commit()
        flash("Danh sách lớp đã được tạo thành công!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Lỗi xảy ra khi tạo danh sách lớp: {str(e)}", "error")

    return redirect('/admin')


if __name__ == '__main__':
    from app import admin
    app.run(debug=True)