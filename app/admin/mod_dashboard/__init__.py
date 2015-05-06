"""
	Dashboard Controller
"""
# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from app import db

mod_admin_dashboard = Blueprint('AdminDashboard', __name__, url_prefix='/admin/dashboard')

@mod_admin_dashboard.route('/', methods=['GET','POST'])
def index():
	return render_template("admin/dashboard/index.html")

# End File: app/admin/mod_dashboard/controllers.py
