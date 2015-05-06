"""
  Access Control List - CONTROLLERS
"""
# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect
from app.helpers.decorators import requires_auth
from app.admin.mod_acl.models import ACL_Roles, ACL_Permissions, ACL_Role_Permissions, ACL_User_Permissions, ACL_User_Roles

mod_admin_acl = Blueprint('AdminAcl', __name__, url_prefix='/admin/acl')

@mod_admin_acl.route('/')
@requires_auth
def index():
  data = {}
  data['roles'] = ACL_Roles.query.all()
  data['perms'] = ACL_Permissions().query.all()
  return render_template("admin/mod_acl/index.html", **data )

@mod_admin_acl.route( '/role_info/<role_id>')
@requires_auth
def role_info( role_id ):
  data = { 'role' : ACL_Roles( role_id ) }
  return render_template("admin/mod_acl/role_info.html", **data )  

@mod_admin_acl.route( '/perm_info/<perm_id>')
@requires_auth
def perm_info( perm_id ):
  data = {}
  data['perm']  = ACL_Permissions( perm_id )
  data['roles'] = ACL_Role_Permissions().for_perm( perm_id ) 
  return render_template("admin/mod_acl/perm_info.html", **data ) 

@mod_admin_acl.route( '/role_add/', methods=['GET','POST'] )
@requires_auth
def role_add():
  if request.method == "POST":
    if request.form['create_type'] == 'role':
      acl_role = ACL_Roles()
      acl_role.role_key  = request.form['role_key']
      acl_role.role_name = request.form['role_name']
      acl_role.save()
  return render_template("admin/mod_acl/role_create.html")

@mod_admin_acl.route( '/perm_add/<role_id>/', methods=['GET','POST'] )
@requires_auth
def perm_add( role_id = None ):
  if request.method == "POST":
    if request.form['create_type'] == 'perm':
      acl_perm = ACL_Permissions()
      acl_perm.perm_key  = request.form['perm_key']
      acl_perm.perm_name = request.form['perm_name']
      acl_perm.save()
      if role_id:
        role_perm = ACL_Role_Permissions()
        role_perm.role_id = role_id
        role_perm.perm_id = acl_perm.id
        role_perm.value   = 1
        role_perm.save()
      return redirect( 'admin/acl/role_info/' + role_id )
  data = {}
  data['role_id'] = role_id
  data['role']    = ACL_Roles( role_id ) 
  data['perms']   = ACL_Permissions( ).get_all()
  return render_template("admin/mod_acl/perm_create.html", **data )

@mod_admin_acl.route( '/role_edit/<role_id>', methods=['GET','POST'] )
@requires_auth
def role_edit( role_id ):
  data = {}
  role = ACL_Roles( role_id = role_id )
  if request.method == "POST":
  	role.user_id = request.form['user_id']
  	role.role_id = request.form['role_id']
  	role.save()
  data['role'] = role
  return render_template("admin/mod_acl/role_edit.html", **data )  

@mod_admin_acl.route( '/perm_edit/<perm_id>', methods=['GET','POST'] )
@requires_auth
def perm_edit( perm_id ):
  data = {}
  perm = ACL_Permissions( perm_id )

  # if request.method == "POST":
    # if request.form['create_type'] == 'role':
      # acl_role = ACL_Roles()
      # acl_role.role_key  = request.form['role_key']
      # acl_role.role_name = request.form['role_name']
      # acl_role.save()
  data['perm'] = perm
  return render_template("admin/mod_acl/perm_edit.html", **data )  

@mod_admin_acl.route( '/role_delete/<role_id>' )
@requires_auth
def role_delete( role_id ):
  ACL_Roles( role_id ).delete()
  return redirect('/admin/acl/')

@mod_admin_acl.route( '/perm_delete/<perm_id>' )
@requires_auth
def perm_delete( perm_id ):
  ACL_Permissions( perm_id ).delete()
  return redirect('/admin/acl/')

@mod_admin_acl.route( '/remove_perm_from_role/<role_id>/<perm_id>' )
@requires_auth
def remove_perm_from_role( role_id, perm_id ):
  role_perm = ACL_Role_Permissions().get_by_role_and_perm( role_id, perm_id )
  role_perm.delete()
  return redirect( '/admin/acl/role_info/' + role_id )

# End File: app/admin/mod_acl/controllers.py
