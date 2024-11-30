from flask import Blueprint, request, render_template, redirect, url_for, flash
from model.nhaxuatban_model import getnxb, them_nxb_new, sua_nxb_new, xoa_nxb_new

# Định nghĩa Blueprint cho Nhà Xuất Bản
nhaxuatban_bp = Blueprint('nhaxuatban', __name__, url_prefix='/nhaxuatban')


# Hiển thị danh sách Nhà Xuất Bản
@nhaxuatban_bp.route('/')
def get_nxb():
    nhaxuatbans = getnxb()  # Lấy danh sách Nhà Xuất Bản từ database
    return render_template('nhaxuatban.html', nhaxuatbans=nhaxuatbans)


# Thêm Nhà Xuất Bản
@nhaxuatban_bp.route('/them', methods=['POST'])
def them_nxb():
    maNXB = request.form.get('maNXB')
    tenNXB = request.form.get('tenNXB')
    ghiChu = request.form.get('ghiChu')

    # Kiểm tra dữ liệu đầu vào
    if not maNXB:
        flash('Vui lòng nhập mã tac gia', 'danger')
        return redirect(url_for('nhaxuatban.get_nxb'))
    if not tenNXB:
        flash('Vui lòng nhập tên loại sách', 'danger')
        return redirect(url_for('nhaxuatban.get_nxb'))

    # Gọi hàm them_loai_sach
    message = them_nxb_new(maNXB, tenNXB, ghiChu)
    if message == "Mã loại sách đã tồn tại":
        flash(message, 'danger')
    elif message == "Thêm nxb thành công!":
        flash(message, 'success')
    else:
        flash(message, 'danger')

    return redirect(url_for('nhaxuatban.get_nxb'))


# Sửa Nhà Xuất Bản
@nhaxuatban_bp.route('/sua', methods=['POST'])
def sua_nxb():
    maNXB = request.form.get('maNXB')
    tenNXB = request.form.get('tenNXB')
    ghiChu = request.form.get('ghiChu')

    if not maNXB or not tenNXB:
        flash('Vui lòng nhập đầy đủ thông tin!', 'danger')
        return redirect(url_for('nhaxuatban.get_nxb'))

    sua_nxb_new(maNXB, tenNXB, ghiChu)
    flash('Cập nhật nxb thành công!', 'success')
    return redirect(url_for('nhaxuatban.get_nxb'))


# Xóa Nhà Xuất Bản
@nhaxuatban_bp.route('/xoa/<maNXB>', methods=['POST'])
def xoa_nxb(maNXB):
    message = xoa_nxb_new(maNXB)
    if message == "Xóa nxb thành công!":
        flash(message, 'success')
    else:
        flash(message, 'danger')  # Hiển thị lỗi nếu không thể xóa

    return redirect(url_for('nhaxuatban.get_nxb'))
