

from flask import Blueprint, request, render_template, redirect, url_for, flash
from model.quanlysinhvien_model import getsinhvien, them_quan_lysinhvien, sua_quan_lysinhvien, xoa_quan_lysinhvien
from model.tacgia_model import them_tac_gia

# Định nghĩa Blueprint
quanlysinhvien_bp = Blueprint('quanlysinhvien', __name__, url_prefix='/quanlysinhvien')


@quanlysinhvien_bp.route('/')
def get_quanlysinhvien():
    quanlysinhviens = getsinhvien()
    return render_template('quanlysinhvien.html', quanlysinhviens=quanlysinhviens)

@quanlysinhvien_bp.route('/them', methods=['POST'])
def them_quanlysinhvien():
    maSinhVien = request.form.get('maSinhVien')
    tenSinhVien = request.form.get('tenSinhVien')
    nganhHoc = request.form.get('nganhHoc')
    khoaHoc = request.form.get('khoaHoc')
    soDienThoai = request.form.get('soDienThoai')
    if not maSinhVien:
        flash('Vui lòng nhập mã sinh vien', 'danger')
        return redirect(url_for('quanlysinhvien.get_quanlysinhvien'))
    if not tenSinhVien:
        flash('Vui lòng nhập tên sinh vien', 'danger')
        return redirect(url_for('quanlysinhvien.get_quanlysinhvien'))

        # Gọi hàm them_loai_sach
    message = them_quan_lysinhvien(maSinhVien, tenSinhVien, nganhHoc, khoaHoc, soDienThoai)
    if message == "Mã sinh vien đã tồn tại":
        flash(message, 'danger')
    elif message == "Thêm sinh vien thành công!":
        flash(message, 'success')
    else:
        flash(message, 'danger')

    return redirect(url_for('quanlysinhvien.get_quanlysinhvien'))

@quanlysinhvien_bp.route('/sua', methods=['POST'])
def sua_quanlysinhvien():
    maSinhVien = request.form.get('maSinhVien')
    tenSinhVien = request.form.get('tenSinhVien')
    nganhHoc = request.form.get('nganhHoc')
    khoaHoc = request.form.get('khoaHoc')
    soDienThoai = request.form.get('soDienThoai')
    if not maSinhVien or not tenSinhVien:
        flash('Vui lòng nhập đầy đủ thông tin!', 'danger')
        return redirect(url_for('quanlysinhvien.get_quanlysinhvien'))

    sua_quan_lysinhvien(maSinhVien, tenSinhVien, nganhHoc,khoaHoc,soDienThoai)
    flash('Cập nhật sinh vien thành công!', 'success')
    return redirect(url_for('quanlysinhvien.get_quanlysinhvien'))


@quanlysinhvien_bp.route('/xoa/<maSinhVien>', methods=['POST'])
def xoa_quanlysinhvien(maSinhVien):
    message = xoa_quan_lysinhvien(maSinhVien)

    if message == "Xóa sinh vien thành công!":
        flash(message, 'success')
    else:
        flash(message, 'danger')  # Hiển thị lỗi nếu không thể xóa

    return redirect(url_for('quanlysinhvien.get_quanlysinhvien'))


