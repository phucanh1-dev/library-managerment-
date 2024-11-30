from functools import wraps
from os import abort

from flask import Blueprint, request, render_template, redirect, url_for, flash, session

from model.quanlynhanvien_model import getnhanvien, them_quan_lynhanien, sua_quan_lynhanvien, xoa_quan_lynhanvien, \
    check_login

quanlynhanvien_bp = Blueprint('quanlynhanvien', __name__, url_prefix='/quanlynhanvien')


@quanlynhanvien_bp.route('/')
def get_quanlynhanvien():
    quanlynhanviens = getnhanvien()
    return render_template('quanlynhanvien.html', quanlynhanviens = quanlynhanviens)



@quanlynhanvien_bp.route('/them', methods=['POST'])
def them_quanlynhanvien():
    maNhanVien = request.form.get('maNhanVien')
    tenNhanVien = request.form.get('tenNhanVien')
    soDienThoai = request.form.get('soDienThoai')
    gioiTinh = request.form.get('gioiTinh')
    diaChi = request.form.get('diaChi')
    matKhau = request.form.get('matKhau')
    vaiTro = request.form.get('vaiTro')



    if len(soDienThoai) != 10 or not soDienThoai.isdigit():
        flash('Số điện thoại phải là 10 số và chỉ chứa chữ số.', 'danger')
        return redirect(url_for('quanlynhanvien.get_quanlynhanvien'))

    if not maNhanVien:
        flash('Vui lòng nhập mã nhan vien', 'danger')
        return redirect(url_for('quanlynhanvien.get_quanlynhanvien'))

    if not tenNhanVien:
        flash('Vui lòng nhập tên nhan vien', 'danger')
        return redirect(url_for('quanlynhanvien.get_quanlynhanvien'))

        # Gọi hàm them_loai_sach
    message = them_quan_lynhanien(maNhanVien, tenNhanVien, soDienThoai, gioiTinh, diaChi, matKhau, vaiTro)
    if message == "Mã nhan vien đã tồn tại":
        flash(message, 'danger')
    elif message == "Thêm nhan vien thành công!":
        flash(message, 'success')
    else:
        flash(message, 'danger')

    return redirect(url_for('quanlynhanvien.get_quanlynhanvien'))


@quanlynhanvien_bp.route('/sua', methods=['POST'])
def sua_quanlynhanvien():
    maNhanVien = request.form.get('maNhanVien')
    tenNhanVien = request.form.get('tenNhanVien')
    soDienThoai = request.form.get('soDienThoai')
    gioiTinh = request.form.get('gioiTinh')
    diaChi = request.form.get('diaChi')
    matKhau = request.form.get('matKhau')
    vaiTro = request.form.get('vaiTro')
    if not maNhanVien or not tenNhanVien:
        flash('Vui lòng nhập đầy đủ thông tin!', 'danger')
        return redirect(url_for('quanlynhanvien.get_quanlynhanvien'))

    sua_quan_lynhanvien(maNhanVien, tenNhanVien, soDienThoai, gioiTinh, diaChi, matKhau, vaiTro)
    flash('Cập nhật sinh vien thành công!', 'success')
    return redirect(url_for('quanlynhanvien.get_quanlynhanvien'))


@quanlynhanvien_bp.route('/xoa/<maNhanVien>', methods=['POST'])
def xoa_quanlynhanvien(maNhanVien):
    message = xoa_quan_lynhanvien(maNhanVien)

    if message == "Xóa nhan vien thành công!":
        flash(message, 'success')
    else:
        flash(message, 'danger')  # Hiển thị lỗi nếu không thể xóa

    return redirect(url_for('quanlynhanvien.get_quanlynhanvien'))


@quanlynhanvien_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']

        user = check_login(phone, password)
        if user:
            # Lưu thông tin người dùng vào session
            session['logged_in'] = True
            session['user_id'] = user[0]  # MaNhanVien
            session['user_name'] = user[1]  # TenNhanVien
            session['role'] = user[2]  # VaiTro

            # In thông tin session ra để kiểm tra
            print(f"User ID: {session['user_id']}, Role: {session['role']}")

            # Điều hướng đến trang chủ hoặc trang quản lý nhân viên tùy thuộc vào vai trò
            if user[2] == 'admin':
                return redirect(url_for('quanlynhanvien.get_quanlynhanvien'))
            else:
                return redirect(url_for('home'))
        else:
            return render_template('dangnhap.html', error="Số điện thoại hoặc mật khẩu không đúng")

    return render_template('dangnhap.html')


@quanlynhanvien_bp.route('/logout')
def logout():
    session.clear()  # Xóa thông tin đăng nhập khỏi session
    return redirect(url_for('quanlynhanvien.login'))  # Điều hướng về trang đăng nhập
