from werkzeug import check_password_hash, generate_password_hash
from app import app
from app import db
from app.admin.mod_acl.models import ACL_Roles, ACL_Permissions, ACL_Role_Permissions, ACL_User_Permissions, ACL_User_Roles
from app.admin.mod_users.models import User
if __name__ == '__main__':
  app.logger.info('Runing Installer')
  db.create_all()

  ### Create Roles 
  acl_role = ACL_Roles()
  acl_role.role_key  = 'super-admin'
  acl_role.role_name = 'Super Admin'
  acl_role.save()

  acl_perm = ACL_Permissions()
  acl_perm.perm_key  = 'access-admin'
  acl_perm.perm_name = 'Access Admin'
  acl_perm.save()

  acl_role_perm = ACL_Role_Permissions()
  acl_role_perm.role_id = 1
  acl_role_perm.perm_id = 1
  acl_role_perm.save()

  user = User( email = app.config['ADMIN_EMAIL'] )
  user.name     = 'Admin'
  user.status   = 'Active'
  user.password = generate_password_hash( app.config['ADMIN_PASSWORD'] )
  user.save()
  
  acl_user_role = ACL_User_Roles()
  acl_user_role.user_id = user.id
  acl_user_role.role_id = 1
  acl_user_role.save()

  app.logger.info( "Created User: %s with Password %s login in at %s " % (
    app.config["ADMIN_EMAIL"],
    app.config["ADMIN_PASSWORD"],
    "http://%s:%s/admin/" % ( app.config["WEB_IP"], app.config["WEB_PORT"] )
    )
  )
# End File install.py
