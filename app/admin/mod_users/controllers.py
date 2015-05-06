"""
    USER - CONTROLLER
"""
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect
from werkzeug import check_password_hash, generate_password_hash

from app.helpers.decorators import *
from app.admin.mod_auth.forms import LoginForm
from app.admin.mod_users.models import User
from app.admin.mod_acl.models import ACL_Roles, ACL_User_Roles

mod_users = Blueprint('AdminUsers', __name__, url_prefix='/admin/users')

@mod_users.route('/', methods=['GET','POST'])
@requires_auth
def index():
    users = User.query.all()
    return render_template('admin/mod_users/roster.html',  **locals() )

@mod_users.route('/info/<user_id>/')
@requires_auth
def info( user_id ):
    """
    /admin/user/info/
    Get the users full information for editing.
    """
    if user_id == 'me':
      user_id = session['user_id']
    data = {}
    data['user'] = User( id = user_id )
    return render_template( "admin/mod_users/info.html", **data )

@mod_users.route('/create/', methods=['GET','POST'])
@requires_auth
def create():
    """
    /admin/user/create/
    """
    if request.method == "POST":
        user = User( email = request.form['user_email'] )
        user.name     = request.form['user_name']
        user.password = generate_password_hash( request.form['user_password']  )
        user.status   = 'active'
        user.save()
        acl_user_role = ACL_User_Roles()
        acl_user_role.user_id = user.id
        acl_user_role.role_id = request.form['user_role_id']
        acl_user_role.save()        
        return redirect('/admin/users')
    else:
        data = {}
        data['roles'] = ACL_Roles.query.all()
        return render_template('admin/mod_users/create.html',  **data )

@mod_users.route('/edit/<user_id>/' , methods=['GET','POST'])
@requires_auth
def edit( user_id = None ):
    """
    /admin/user/edit/<user_id>
    """
    if user_id == 'me':
      user_id = session['user_id']
    user = User( id = user_id )
    if request.method == "POST":
        user.name     = request.form['user_name']
        user.email    = request.form['user_email']
        if 'user_password' in request.form and request.form['user_password'] not in [ None, '' ]:
            # if request.form['user_password'] != request.form['user_password2']:
            #     return redirect('/admin/users/edit/' + user_id )
            user.password = generate_password_hash( request.form['user_password'] )
        user.save()
        acl_user_role = ACL_User_Roles()
        acl_user_role.user_id = user.id
        acl_user_role.role_id = request.form['user_role_id']
        acl_user_role.save()
        return redirect('/admin/users/info/' + user_id )
    else:
        data = {}
        data['user']  = user
        data['roles'] = ACL_Roles.query.all()
        return render_template('admin/mod_users/edit.html', **data )

@mod_users.route('/delete/<user_id>/')
@requires_auth
def delete( user_id ):
    """
    /admin/users/delete/<user_id>
    """
    User( user_id ).delete()
    return redirect('/admin/users')

# from system.admin.controllers import BASECTRLAdminUsers

# class CTRLAdminUsers( BASECTRLAdminUsers ):
    
#     @requires_auth
#     def __init__( self ):
#         self.something = 'yeah thats something'
#         app.log.debug( 'were making an admin user page now' )

#     @mod_users.route('/testing/')
#     def test_shit():
#         return 'yeahhh'
#         # return self.something

# End File: app/admin/mod_user/controllers.py 
