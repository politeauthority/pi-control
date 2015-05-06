"""
  ACCESS CONTROL LIST - MODELS
"""
from flask import session
from flask import current_app as app
from app import db

class Base(db.Model):

  __abstract__  = True

  id            = db.Column(db.Integer, primary_key=True)
  date_created  = db.Column(db.DateTime, default=db.func.current_timestamp())
  date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                                         onupdate=db.func.current_timestamp())
  def save( self ):
    if self.id == None:
      new_obj = self
      db.session.add( new_obj )
    db.session.commit()

  def delete( self ):
    if self.id:
      delete = self.query.filter( self.id == self.id ).first()
      if not delete:
        return False
      db.session.delete( delete )
      db.session.commit()
      return True
    return False

class ACL( object ):

  def get_access_by_user( self, user_id ):
    #session.pop( 'perms', None )
    if 'perms' not in session:
      roles = ACL_User_Roles.query.filter( ACL_User_Roles.user_id == user_id ).all()
      perms = []
      for role in roles:
        for p in ACL_Role_Permissions().for_role( role.role_id ):
          perms.append( p )
      permissions = set()
      for p in perms:
        permissions.add( p.perm_key )
      #session['perms'] = permissions
      return permissions

  def check_permission( self, perm_key, user_id = None ):
    s = 'User: ' + str( user_id )
    s+= 'perm_key: ' +  str( perm_key )
    user_access = self.get_access_by_user( user_id )
    if perm_key in user_access:
      return True
    else:
      return False

class ACL_Roles(Base):
    
  __tablename__ = 'acl_roles'
  role_key  = db.Column(db.String(25) , nullable=False)
  role_name = db.Column(db.String(128) , nullable=False)

  def __init__( self, role_id = None ):
    if role_id:
      r = self.query.filter( ACL_Roles.id == role_id ).first()
      if r:
        self.id            = role_id
        self.role_key      = r.role_key
        self.role_name     = r.role_name
        self.date_created  = r.date_created
        self.date_modified = r.date_modified
        self.permissions   = ACL_Role_Permissions().for_role( role_id )
  
  def get_permissions( self ):
    role_permissions = ACL_Role_Permissions.query.filter( ACL_Role_Permissions.role_id )

class ACL_Permissions(Base):

  __tablename__ = 'acl_permissions'
  perm_key  = db.Column(db.String(25) , nullable=False)
  perm_name = db.Column(db.String(128) , nullable=False)

  def __init__( self, perm_id = None ):
    if perm_id:
        p = self.query.filter( ACL_Permissions.id == perm_id ).first()
        if p:
          self.id            = perm_id
          self.perm_key      = p.perm_key
          self.perm_name     = p.perm_name
          self.date_created  = p.date_created
          self.date_modified = p.date_modified

  def get_all( self ):
    permissions = self.query.filter().all()
    return permissions

class ACL_Role_Permissions(Base):

    __tablename__ = 'acl_role_permissions'
    role_id = db.Column(db.Integer)
    perm_id = db.Column(db.Integer)
    value   = db.Column(db.Integer)

    def __init__( self, rp_id = None ):
      if rp_id:
          rp = self.query.filter( ACL_Role_Permissions.id == rp_id )
          #if rp:
            #self.id            = rp_id
            #self.role_id       = rp.role_id
            #self.perm_id       = rp.perm_id
            #self.value         = rp.value
            #self.date_created  = rp.date_created
            #self.date_modified = rp.date_modified

    def get_by_role_and_perm( self, role_id, perm_id ):
      role_permission = self.query.filter( ACL_Role_Permissions.role_id == role_id, ACL_Role_Permissions.perm_id == perm_id ).all()
      if len( role_permission ) == 0:
        return False
      return role_permission[0]

    def for_user( self, user_id ):
    	the_roles = []
    	for user_role in ACL_User_Roles.query.filter( ACL_User_Roles.user_id == user_id ).all():
    		the_roles.append( ACL_Roles( user_role.role_id ) )
    	return the_roles

    def for_perm( self, perm_id ):
      the_roles = []
      for acl_role_perm in self.query.filter( ACL_Role_Permissions.perm_id == perm_id ).all():
        the_roles.append( ACL_Roles( acl_role_perm.role_id ) )      
      return the_roles

    def for_role( self, role_id ):
      the_perms = []
      for acl_role_perm in self.query.filter( ACL_Role_Permissions.role_id == role_id ).all():
        the_perms.append( ACL_Permissions( acl_role_perm.perm_id ) )
      return the_perms

class ACL_User_Roles(Base):

  __tablename__ = 'acl_user_roles'
  user_id = db.Column(db.Integer)
  role_id = db.Column(db.Integer)
  #  UNIQUE KEY `user_id` (`user_id`,`role_id`)

  def __init__( self, user_role_id = None ):
    if user_role_id:
      ur = self.query.filter( ACL_User_Roles.id == user_role_id ).all()
      if ur:
        self.id            = user_role_id
        self.user_id       = ur.user_id
        self.role_id       = ur.role_id
        self.date_created  = ur.date_created
        self.date_modified = ur.date_modified

  def __repr__(self):
    return '<ACL_UserRole Role %r,  User %r>' % (self.role_id, self.user_id)

  def get_by_user( self, user_id ):
    acl_user_role = self.query.filter( ACL_User_Roles.user_id == user_id ).all()
    if len( acl_user_role ) != 1:
      return False
    return ACL_Roles( role_id = acl_user_role[0].role_id )

class ACL_User_Permissions(Base):

  __tablename__ = 'acl_user_permissions'
  user_id = db.Column(db.Integer)
  perm_id = db.Column(db.Integer)
  value   = db.Column(db.Integer)
  #  UNIQUE KEY `user_id` (`user_id`,`perm_id`)

  def __init__( self, user_permission_id = None ):
    if user_permission_id:
      up = self.query.filter( ACL_User_Permissions.id == user_permission_id ).all()
      if up:
        self.id            = user_permission_id
        self.user_id       = up.user_id
        self.perm_id       = up.perm_id
        self.date_created  = up.date_created
        self.date_modified = up.date_modified

# End File: app/admin/mod_acl/models.py
