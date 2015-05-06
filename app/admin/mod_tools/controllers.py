# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from app import db
from app.helpers.decorators import requires_auth
from app.admin.mod_users.models import User
# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_admin_tools = Blueprint('AdminTools', __name__, url_prefix='/admin/tools')

@mod_admin_tools.route('/')
@requires_auth
def index():
  return render_template('admin/mod_tools/index.html')

@mod_admin_tools.route('/change_user/', methods=['GET','POST'] )
@requires_auth
def change_user():
  if request.method == "POST":
    session['user_id'] = request.form['user_id']
    return redirect('/')
  data = {}
  data['users'] = User().get_all()

  return render_template( 'admin/mod_tools/change_user.html', **data )

@mod_admin_tools.route('/themes/')
@requires_auth
def themes():
  return render_template('admin/mod_tools/themes.html')

# End File: app/admin/mod_tools/controllers.py
