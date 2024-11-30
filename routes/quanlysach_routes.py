from flask import Blueprint, request, render_template, redirect, url_for, flash
from model.quanlysach_model import getquanlysach
from routes.sach_routes import sach_bp

# Định nghĩa Blueprint
quanlysach_bp = Blueprint('quanlysach', __name__, url_prefix='/quanlysach')




@quanlysach_bp.route('/')
def get_quanlysach():
    quanlysachs = getquanlysach()
    return render_template('quanlysach.html', quanlysachs=quanlysachs)


