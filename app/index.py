from flask import Flask, render_template, request, redirect, session, flash
from sqlalchemy.testing.plugin.plugin_base import config

from app import app, db
from datetime import date,datetime
from app.models import NhanVien, HocSinh

app.secret_key = 'secret_key'  # Khóa bảo mật cho session

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        taiKhoan = request.form['taiKhoan']
        matKhau = request.form['matKhau']
        nv = NhanVien.query.filter_by(taiKhoan=taiKhoan).first()
        if nv and nv.check_password(matKhau) and nv.get_VaiTro()=="Nhân Viên Tiếp Nhận":
            session['logged_in'] = True
            session['idNhanVien'] = nv.idNhanVien
            session['hoTen'] = nv.hoTen
            return redirect('/dashboard')
        else:
            flash('Sai tài khoản hoặc mật khẩu!', 'danger')
            return redirect('/login')
    return render_template('layout/login.html')


@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect('/login')
    return render_template('layout/dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.before_request
def require_login():
    allowed_routes = ['login', 'logout']
    if request.endpoint not in allowed_routes and not session.get('logged_in'):
        return redirect('/login')

@app.route('/nhap-ho-so', methods=['POST'])
def kiem_tra_tuoi():
    if 'logged_in' not in session:
        return redirect('/login')

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
            return redirect('/dashboard')
    return "Không nhận được thông tin ngày sinh!"

@app.route('/luu-hoc-sinh', methods=['POST'])
def luu_hoc_sinh():
    if 'logged_in' not in session:
        return redirect('/login')

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
        eMail=email
    )
    db.session.add(hoc_sinh)
    db.session.commit()

    flash("Học sinh đã được lưu thành công!", "success")
    return redirect("/dashboard")


if __name__ == '__main__':
    app.run(debug=True)