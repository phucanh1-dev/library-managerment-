from flask import Blueprint, request, render_template, redirect, url_for, flash
from model.danhsachquahan_model import getdanhsachquahan
from model.quanlybaocaothongke_model import gettongsach, gettongloaisach, gettongtacgia, gettongnhaxuatban, gettongsinhvien, gettongsachmuon, gettongnhanvien


danhsachquahan_bp = Blueprint('danhsachquahan', __name__, url_prefix='/danhsachquahan')


@danhsachquahan_bp.route('/')
def get_danhsachquahan():
    danhsachquahans = getdanhsachquahan()
    tongsachs = gettongsach()
    tongloaisachs = gettongloaisach()
    tongtacgias = gettongtacgia()
    tongnhaxuatbans = gettongnhaxuatban()
    tongsinhviens = gettongsinhvien()
    tongsachmuons = gettongsachmuon()
    tongnhanviens = gettongnhanvien()
    return render_template('danhsachquahan.html',danhsachquahans=danhsachquahans, tongsachs=tongsachs, tongloaisachs=tongloaisachs, tongtacgias=tongtacgias, tongnhaxuatbans=tongnhaxuatbans, tongsinhviens=tongsinhviens, tongsachmuons=tongsachmuons, tongnhanviens=tongnhanviens)





