from flask import Blueprint, request, render_template, redirect, url_for, flash

from model.loaisach_model import getloaisach
from model.nhaxuatban_model import getnxb
from model.sach_model import getsach, them_sach_new, sua_sach_new, xoa_sach_new
from model.tacgia_model import gettacgia

sach_bp = Blueprint('sach', __name__, url_prefix='/sach')


@sach_bp.route('/')
def get_sach():
    sachs = getsach()
    tacgias=gettacgia()
    nhaxuatbans=getnxb()
    loaisachs=getloaisach()
    return render_template('sach.html',sachs=sachs, tacgias=tacgias, nhaxuatbans=nhaxuatbans, loaisachs=loaisachs)


@sach_bp.route('/them', methods=['POST'])
def them_sach():
    maSach = request.form.get('maSach')
    tenSach = request.form.get('tenSach')
    tacGia = request.form.get('tacGia')  # Lấy mã tác giả
    nhaXuatBan = request.form.get('nhaXuatBan')
    loaiSach = request.form.get('loaiSach')
    soTrang = request.form.get('soTrang')
    giaBan = request.form.get('giaBan')
    soLuong = request.form.get('soLuong')
    hinhAnh = request.form.get('hinhAnh')

    # Kiểm tra dữ liệu hợp lệ
    if not maSach:
        flash('Vui lòng nhập mã sach', 'danger')
        return redirect(url_for('sach.get_sach'))
    if not tenSach:
        flash('Vui lòng nhập tên sach', 'danger')
        return redirect(url_for('sach.get_sach'))

        # Gọi hàm them_loai_sach
    message = them_sach_new(maSach, tenSach, tacGia,nhaXuatBan,loaiSach,soTrang,giaBan,soLuong,hinhAnh)
    if message == "Mã Sach đã tồn tại":
        flash(message, 'danger')
    elif message == "Thêm sách thành công!":
        flash(message, 'success')
    else:
        flash(message, 'danger')

    return redirect(url_for('sach.get_sach'))

@sach_bp.route('/sua', methods=['POST'])
def sua_sach():
    maSach = request.form.get('maSach')
    tenSach = request.form.get('tenSach')
    tacGia = request.form.get('tacGia')  # Lấy mã tác giả
    nhaXuatBan = request.form.get('nhaXuatBan')
    loaiSach = request.form.get('loaiSach')
    soTrang = request.form.get('soTrang')
    giaBan = request.form.get('giaBan')
    soLuong = request.form.get('soLuong')
    hinhAnh = request.form.get('hinhAnh')

    if not maSach or not tenSach:
        flash('Vui lòng nhập đầy đủ thông tin!', 'danger')
        return redirect(url_for('sach.get_sach'))

    sua_sach_new(maSach, tenSach, tacGia,nhaXuatBan,loaiSach,soTrang,giaBan,soLuong,hinhAnh)
    flash("Cập nhật sách thành công!", 'success')
    return redirect(url_for('sach.get_sach'))

@sach_bp.route('/xoa/<maSach>', methods=['POST'])
def xoa_sach(maSach):
    message = xoa_sach_new(maSach)

    if message == "Xóa sach thành công!":
        flash(message, 'success')
    else:
        flash(message, 'danger')  # Hiển thị lỗi nếu không thể xóa

    return redirect(url_for('sach.get_sach'))