# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from app import db

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_admin_home = Blueprint('Admin', __name__, url_prefix='/admin')

@mod_admin_home.route('/', methods=['GET','POST'])
def index():
    return redirect('/admin/auth/')

# End File: app/admin/mod_home/controllers.py
