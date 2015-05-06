"""
	DASHBOARD - CONTROLLERS
"""
# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect
from flask import current_app as app
from app.helpers.decorators import requires_auth
from app.helpers import misc
import os

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_admin_dashboard = Blueprint('AdminDashboard', __name__, url_prefix='/admin/dashboard')

@mod_admin_dashboard.route('/')
@requires_auth
def index():
	data = {}
	data['upload_dir_size'] = str( misc.directory_size( app.config['UPLOAD_DIR'] )  / 1048576 ) + 'Mb'
	data['cachie_dir_size'] = str( misc.directory_size( app.config['CACHE_DIR'] )  / 1048576 ) + 'Mb'
	return render_template("admin/mod_dashboard/index.html", **data)

# End File: app/admin/mod_dashboard/controllers.py
