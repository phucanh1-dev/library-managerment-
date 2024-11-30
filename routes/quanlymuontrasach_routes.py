from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from model.quanlymuontrasach_model import getmuontrasach, muonsach, trasach, giahan_ngaytra
from model.quanlysach_model import getquanlysach
from model.sach_model import getsach
from model.quanlysinhvien_model import getsinhvien
quanlymuontrasach_bp = Blueprint('quanlymuontrasach', __name__, url_prefix='/quanlymuontrasach')

@quanlymuontrasach_bp.route('/')
def get_quanlymuontrasach():
    quanlysachs = getquanlysach()
    sachs = getsach()
    quanlysinhviens = getsinhvien()
    muontrasachs = getmuontrasach()
    return render_template('quanlymuontrasach.html', quanlysachs=quanlysachs, sachs=sachs, muontrasachs=muontrasachs, quanlysinhviens=quanlysinhviens)

@quanlymuontrasach_bp.route('/muon', methods=['POST'])
def them_muonsach():
    txtMaSV = request.form['maSinhVien']
    txtMaSach = request.form['tenSach']
    txtNgayMuon = request.form['ngayMuon']
    txtNgayTra = request.form['ngayTra']
    txtGhiChu = request.form['ghiChu']

    result = muonsach(txtMaSV, txtMaSach, txtNgayMuon, txtNgayTra, txtGhiChu)

    if result.startswith("success"):
        flash("Mượn sách thành công", "success")
    elif result.startswith("error"):
        flash(result.split(":")[1], "error")
    
    return redirect(url_for('quanlymuontrasach.get_quanlymuontrasach'))

@quanlymuontrasach_bp.route('/tra/<int:maPhieuMuon>', methods=['POST'])
def tra_sach(maPhieuMuon):
    result = trasach(maPhieuMuon)

    if result.startswith("success"):
        flash("Trả sách thành công", "success")
    elif result.startswith("error"):
        flash(result.split(":")[1], "error")
    
    return redirect(url_for('quanlymuontrasach.get_quanlymuontrasach'))

@quanlymuontrasach_bp.route('/giahan/<int:maPhieuMuon>', methods=['POST'])
def gia_han_sach(maPhieuMuon):
    txtNgayTraMoi = request.form['ngayTraMoi']

    # Gọi hàm xử lý trong model
    result = giahan_ngaytra(maPhieuMuon, txtNgayTraMoi)

    if result.startswith("success"):
        flash("Gia hạn ngày trả sách thành công", "success")
    elif result.startswith("error"):
        flash(result.split(":")[1], "error")

    return redirect(url_for('quanlymuontrasach.get_quanlymuontrasach'))
