from random import choice
from flask import Flask, render_template, request, redirect, session, flash, url_for, jsonify
from sqlalchemy import Nullable
from sqlalchemy.testing.plugin.plugin_base import config

from app import app, db, dao, login
from datetime import date, datetime

from app.admin import DanhSachLopView
from app.models import NhanVien, HocSinh, UserRole, DanhSachLop, PhongHoc, HocKy, GiaoVienChuNhiem, GiaoVien
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
            return redirect('/nhan-vien')
        elif nv and nv.get_VaiTro() == UserRole.NGUOIQUANTRI:
            login_user(nv)
            return redirect('/admin')
        else:
            err_msg = "Sai tài khoản/ mật khẩu"
    return render_template('layout/login.html', err_msg=err_msg)


@app.route('/nhan-vien')
def dashboard():
    return render_template('layout/nhan_vien.html')


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
        tuoi = hom_nay.year - ngay_sinh.year

        # Kiểm tra tuổi
        if app.config["MIN_AGE"] <= tuoi <= app.config["MAX_AGE"]:
            flash("Tuổi hợp lệ. Hãy nhập thông tin chi tiết.", "success")
            return render_template('layout/nhap_thong_tin_hoc_sinh.html', ngay_sinh=ngay_sinh)
        else:
            flash(f"Tuổi không phù hợp: {tuoi} tuổi!!!", "warning")
            return redirect('/nhan-vien')
    return "Không nhận được thông tin ngày sinh!"


@app.route('/luu-hoc-sinh', methods=['POST'])
def luu_hoc_sinh():
    # Lấy thông tin từ form
    ho_ten = request.form.get('hoTen')
    gioi_tinh = request.form.get('gioiTinh')  # Nam = 1, Nữ = 0
    ngay_sinh = request.form.get('ngaySinh')
    khoi = request.form.get('khoi')
    dia_chi = request.form.get('diaChi')
    so_dien_thoai = request.form.get('soDienThoai')
    email = request.form.get('email')

    # Tạo đối tượng học sinh mới
    hoc_sinh = HocSinh(
        hoTen=ho_ten,
        gioiTinh=(gioi_tinh == '1'),
        ngaySinh=datetime.strptime(ngay_sinh, "%Y-%m-%d").date(),
        khoi=khoi,
        diaChi=dia_chi,
        SDT=so_dien_thoai,
        eMail=email,
        maDsLop=None
    )
    db.session.add(hoc_sinh)
    db.session.commit()

    flash("Học sinh đã được lưu thành công!", "success")
    return redirect("/nhan-vien")


@app.route('/danh-sach-lop')
def show_ds_lop():
    dsLop = DanhSachLop.query.filter(DanhSachLop.active == True)
    return render_template('layout/danh_sach_lop.html', danh_sach_lop=dsLop)


@app.route('/danh-sach-lop/sua/<int:id>', methods=['GET', 'POST'])
def sua_ds_lop(id):
    lop = DanhSachLop.query.filter(DanhSachLop.maDsLop == id).first()

    # Lấy danh sách phòng học chưa được chọn
    list_phong = PhongHoc.query.all()
    list_phong_da_chon = {l.idPhongHoc for l in DanhSachLop.query.filter(DanhSachLop.idPhongHoc != None)}
    list_phong = [phong for phong in list_phong if
                  phong.idPhongHoc not in list_phong_da_chon or phong.idPhongHoc == lop.idPhongHoc]

    list_hs = {hs for hs in HocSinh.query.filter(HocSinh.maDsLop == lop.maDsLop)}

    if request.method == 'POST':
        try:
            # Cập nhật thông tin
            lop.tenLop = request.form.get("tenLop")
            lop.idPhongHoc = int(request.form.get("phongHoc"))
            db.session.commit()
            flash("Cập nhật thông tin lớp thành công", "success")
            return redirect('/danh-sach-lop')  # Chuyển về trang danh sách lớp
        except Exception as e:
            db.session.rollback()
            flash(f"Lỗi khi lưu dữ liệu: {str(e)}", "danger")
            return redirect(request.url)

    return render_template('layout/sua_lop.html', lop=lop, danh_sach_phong=list_phong, danh_sach_hoc_sinh=list_hs)


@app.route('/them-hoc-sinh/<int:id>', methods=['GET', 'POST'])
def them_hoc_sinh(id):
    lop = DanhSachLop.query.filter(DanhSachLop.maDsLop == id).first()

    ds_hs_chua_lop = HocSinh.query.filter(HocSinh.maDsLop == None)

    if request.method == 'POST':
        print(request.form)
        try:
            list_hs_ids = request.form.getlist("hocSinh")  # Lấy danh sách ID học sinh
            if not list_hs_ids:
                flash("Vui lòng chọn ít nhất một học sinh!", "danger")
                return redirect(request.url)

            si_so_hien_tai = HocSinh.query.filter(HocSinh.maDsLop == id).count()
            so_hoc_sinh_them = len(list_hs_ids)
            si_so_moi = si_so_hien_tai + so_hoc_sinh_them

            if si_so_moi > app.config["SI_SO"]:
                flash("Không thể thêm vì vượt quá sĩ số lớp!", "danger")
                return redirect(request.url)
            else:
                lop.siSo = si_so_moi
                db.session.add(lop)
                db.session.commit()

            for hoc_sinh_id in list_hs_ids:
                hoc_sinh = HocSinh.query.get(hoc_sinh_id)
                hoc_sinh.maDsLop = id
                db.session.add(hoc_sinh)
                db.session.commit()

            flash(f"Đã thêm {so_hoc_sinh_them} học sinh vào lớp!", "success")
            return redirect(f'/danh-sach-lop/sua/{id}')
        except Exception as e:
            db.session.rollback()
            flash(f"Lỗi khi thêm học sinh: {str(e)}", "danger")
            return redirect(request.url)

    return render_template('layout/them_hoc_sinh.html', danh_sach_hoc_sinh=ds_hs_chua_lop, lop=lop)


@app.route('/xoa-hoc-sinh', methods=['POST'])
def xoa_hoc_sinh():
    id_hoc_sinh = request.form.get('idHocSinh')  # Lấy ID từ form
    if id_hoc_sinh:
        print(f"ID học sinh nhận được: {id_hoc_sinh}")  # In ra log kiểm tra
        # Kiểm tra và xóa học sinh khỏi database
        hoc_sinh = HocSinh.query.filter_by(idHocSinh=id_hoc_sinh).first()
        if hoc_sinh:
            hoc_sinh.maDsLop = None  # Gỡ học sinh khỏi lớp
            db.session.commit()
            flash('Đã xóa học sinh khỏi danh sách lớp thành công!', 'success')
        else:
            flash('Không tìm thấy học sinh!', 'danger')
        return redirect(url_for('show_ds_lop'))  # Chuyển hướng về danh sách lớp
    flash('Không nhận được ID học sinh để xóa!', 'danger')
    return redirect(url_for('show_ds_lop'))


@app.route('/tao-danh-sach-lop')
def create_auto_classes():
    try:
        # Lấy toàn bộ danh sách học sinh chưa được gán lớp
        students = HocSinh.query.filter(HocSinh.maDsLop == None).all()
        if not students:
            flash("Không có học sinh nào để tạo lớp!", "error")
            return redirect('/admin')

        # Nhóm học sinh theo khối
        grade_groups = {
            "10": [],
            "11": [],
            "12": []
        }
        for student in students:
            if student.khoi == "Khối 10":
                grade_groups["10"].append(student)
            elif student.khoi == "Khối 11":
                grade_groups["11"].append(student)
            elif student.khoi == "Khối 12":
                grade_groups["12"].append(student)

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
        for khoi, group_students in grade_groups.items():
            batch_size = app.config["SI_SO"]  # Số lượng học sinh mỗi lớp
            for i in range(0, len(group_students), batch_size):
                class_students = group_students[i:i + batch_size]

                # Chọn giáo viên ngẫu nhiên
                giao_vien_CN = choice(giao_vien_list)

                # Tạo danh sách lớp mới
                new_class = DanhSachLop(
                    # Gán phòng học
                    tenLop=f"{khoi}",
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
