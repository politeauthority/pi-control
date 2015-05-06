"""
    Misc - HELPER
"""
#from flask import g, session, redirect
#from flask import current_app as app
#from app.admin.mod_acl.models import ACL
#from app.admin.mod_users.models import User
import os

def directory_size( the_dir ):
  total_size = 0
  for dirpath, dirnames, filenames in os.walk( the_dir ):
    for f in filenames:
      fp = os.path.join(dirpath, f)
      total_size += os.path.getsize(fp)
  return total_size

def make_slug( butterfly ):
  slug = butterfly.lower()
  slug = slug.replace( ' ', '-' )
  slug = slug.replace( '_', '-' )
  slug = slug.replace( "---", '-' )  
  slug = slug.replace( '!', '' )
  slug = slug.replace( '@', '' )
  slug = slug.replace( '#', '' )
  slug = slug.replace( '$', '' )
  slug = slug.replace( '%', '' )
  slug = slug.replace( '^', '' )
  slug = slug.replace( '&', '' )
  slug = slug.replace( '*', '' )
  slug = slug.replace( '(', '' )
  slug = slug.replace( ')', '' )
  slug = slug.replace( '=', '' )
  slug = slug.replace( '+', '' )
  slug = slug.replace( '[', '' )
  slug = slug.replace( ']', '' )
  slug = slug.replace( '{', '' )
  slug = slug.replace( '}', '' )
  slug = slug.replace( '/', '' )
  slug = slug.replace( '|', '' )
  slug = slug.replace( ';', '' )
  slug = slug.replace( ':', '' )
  slug = slug.replace( '.', '' )
  slug = slug.replace( '>', '' )
  slug = slug.replace( '<', '' )
  slug = slug.replace( '?', '' )
  slug = slug.replace( '`', '' )
  slug = slug.replace( '~', '' )
  slug = slug.replace( '"', '' )
  slug = slug.replace( "'", '' )
  slug = slug.replace( ",", '' )
  return slug

# End File: app/helpers/misc.py
