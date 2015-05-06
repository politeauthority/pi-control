"""
    DECORATORS - HELPER
"""

from functools import wraps
# Import flask dependencies
from flask import g, session, redirect
from flask import current_app as app
from app.admin.mod_acl.models import ACL
from app.admin.mod_users.models import User

# Setup Auth Decorator
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' in session and session['user_id']:
            session['authenticated'] = True
            permission = ACL().check_permission( 'access-admin', session['user_id'] )
            if permission:
              return f(*args, **kwargs)
            else:
              session.pop('user_id', None)
              return redirect('/error/auth')
        else:
            app.logger.warning('Someone trying to access content they cant') 
            app.logger.warning( session )
            session.pop('user_id', None)
            return redirect('/admin/auth/')
    return decorated


# def requires_auth( permission_key ):
#   def decorator(fn):
#     def wrapped_function(*args, **kwargs):
#       if 'user_id' not in session or not session['user_id']:
#         return redirect('/admin/auth/')
      
#       permission = ACL().check_permission( permission_key, session['user_id'] )
#       if not permission:
#         abort(403)
#       return fn(*args, **kwargs)
#     return update_wrapper(wrapped_function, fn)
#   return decorator


# End File: app/helpers/decorators.py
