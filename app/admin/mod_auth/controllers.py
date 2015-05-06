# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect
from app import db
from app.admin.mod_users.models import User
from app.admin.mod_auth.forms import LoginForm

mod_admin_auth = Blueprint('AdminLogin', __name__, url_prefix='/admin/auth')

@mod_admin_auth.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        if request.form['user_password'] == '' or request.form['user_email'] == '':
            return redirect('/admin/auth')
        user = User( email = request.form['user_email'] )
        if user:
            auth = user.auth( request.form['user_password'] )
            if auth:
                session['user_id'] = user.id
                session['authenticated'] = True
                user = User( session['user_id'] )
                session['user'] = {
                    'name'  : user.name,
                    'email' : user.email
                }                
                return redirect('/admin/dashboard/')
    elif 'authenticated' in session and session['authenticated']:
        return redirect('/admin/dashboard/')
    return render_template("admin/mod_auth/login.html")

@mod_admin_auth.route('/logout/')
def logout():
    session.clear()
    return redirect('/')

# End File: app/admin/mod_auth/controllers.py
