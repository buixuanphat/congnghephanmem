from random import choice
from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
from sqlalchemy import Nullable
from sqlalchemy.testing.plugin.plugin_base import config

from app import app, db, dao, login
from datetime import date, datetime
from app.models import NhanVien, HocSinh, UserRole, DanhSachLop, PhongHoc, HocKy, GiaoVienChuNhiem, GiaoVien, KhoiPhong
from flask_login import login_user, logout_user

app.secret_key = 'secret_key'  # Khóa bảo mật cho session


@app.route('/')
def index():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login_process():
    err_msg = None
    if request.method == 'POST':
        taiKhoan = request.form['taiKhoan']
        matKhau = request.form['matKhau']

        nv = dao.auth_user(taikhoan=taiKhoan, matkhau=matKhau)
        if nv and nv.get_VaiTro() == UserRole.NHANVIENTIEPNHAN:
            login_user(nv)
            return redirect('/nhan-vien-tiep-nhan')
        elif nv and nv.get_VaiTro() == UserRole.NGUOIQUANTRI:
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
        maDsLop=None
    )
    db.session.add(hoc_sinh)
    db.session.commit()

    flash("Học sinh đã được lưu thành công!", "success")
    return redirect("/nhan-vien-tiep-nhan")


@app.route('/tao-danh-sach-lop')
def create_auto_classes():
    try:
        # Lấy toàn bộ danh sách học sinh chưa được gán lớp
        students = HocSinh.query.filter(HocSinh.maDsLop == None).all()
        if not students:
            flash("Không có học sinh nào để tạo lớp!", "error")
            return redirect('/admin')

        def calculate_age(birthdate):
            today = date.today()
            return today.year - birthdate.year

        age_groups = {}
        for student in students:
            age = calculate_age(student.ngaySinh)
            if age not in age_groups:
                age_groups[age] = []
            age_groups[age].append(student)

        # Lấy học kỳ hiện tại
        hoc_ky = HocKy.query.order_by(HocKy.idHocKy.desc()).first()
        if not hoc_ky:
            return jsonify({"error": "Học kỳ không tồn tại"}), 400

        # Lấy danh sách giáo viên chưa gán vào lớp
        giao_vien_list = GiaoVien.query.all()
        giao_vien_da_gan = {gv.idGiaoVien for gv in GiaoVienChuNhiem.query.all()}
        giao_vien_list = [gv for gv in giao_vien_list if gv.idGiaoVien not in giao_vien_da_gan]
        if not giao_vien_list:
            return jsonify({"error": "Không có giáo viên để gán"}), 400

        # Xử lý tạo lớp cho từng nhóm tuổi
        for age, group_students in age_groups.items():
            batch_size = 2  # Số lượng học sinh mỗi lớp
            for i in range(0, len(group_students), batch_size):
                class_students = group_students[i:i + batch_size]

                khoi_phong_su_dung = {ds.maDsLop for ds in DanhSachLop.query.all()}
                khoi_phong_kha_dung = KhoiPhong.query.filter(~KhoiPhong.id.in_(khoi_phong_su_dung)).all()
                if not khoi_phong_kha_dung:
                    flash("Không còn khối phòng khả dụng để tạo lớp!", "error")
                    return redirect('/admin')

                # Chọn giáo viên ngẫu nhiên
                giao_vien_CN = choice(giao_vien_list)

                # Tạo danh sách lớp mới
                new_class = DanhSachLop(
                    khoiPhong_id=khoi_phong_kha_dung.id,  # Gán phòng học
                    tenLop = None,
                    giaoVienChuNhiem_id=giao_vien_CN.idGiaoVien,
                    siSo=len(class_students),
                    hocKy_id=hoc_ky.idHocKy  # Học kỳ hiện tại
                )
                db.session.add(new_class)
                db.session.commit()

                # Thêm giáo viên chủ nhiệm vào bảng GiaoVienChuNhiem
                giao_vien_chu_nhiem = GiaoVienChuNhiem(
                    idGiaoVien=giao_vien_CN.idGiaoVien,
                    idDsLop=new_class.maDsLop
                )
                db.session.add(giao_vien_chu_nhiem)
                db.session.commit()

                # Loại giáo viên vừa gán khỏi danh sách giáo viên khả dụng
                giao_vien_list.remove(giao_vien_CN)

                # Gán học sinh vào lớp vừa tạo
                for student in class_students:
                    student.maDsLop = new_class.maDsLop
                    db.session.add(student)

        db.session.commit()
        flash("Danh sách lớp đã được tạo thành công theo độ tuổi!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Lỗi xảy ra khi tạo danh sách lớp: {str(e)}", "error")

    return redirect('/admin')



if __name__ == '__main__':
    from app import admin

    app.run(debug=True)
