import os
import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, render_template, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension


# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Set Up Logging
app_log_file = os.path.join( app.config['LOG_DIR'], 'app.log' )
logging.basicConfig( filename = app_log_file, level=logging.DEBUG )
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = TimedRotatingFileHandler( 
	app_log_file,
	when='midnight', 
	backupCount=20 )
file_handler.setLevel( logging.DEBUG )
file_handler.setFormatter( formatter )
app.logger.addHandler( file_handler )

console_handler = logging.StreamHandler()
console_handler.setFormatter( formatter )
console_handler.setLevel( logging.DEBUG )
app.logger.addHandler( console_handler )

werkzeug_log = logging.getLogger( 'werkzeug' )
werkzeug_log.setLevel( logging.DEBUG )
# werkzeug_log.setFormatter( formatter )
werkzeug_log.addHandler( file_handler )
werkzeug_log.addHandler( console_handler )

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

toolbar = DebugToolbarExtension( app )
# import helpers.jinja_funcs
# from app.helpers import jinja_funcs

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
	return redirect('/404')

# # Front End BluePrints
from app.frontend.mod_home.controllers import mod_home as home_module
from app.frontend.mod_blog.controllers import mod_blog as blog_module

from app.controllers.media.controllers import media as media_module

# Admin BluePrints
from app.admin.mod_acl.controllers       import mod_admin_acl       as admin_acl_module
from app.admin.mod_auth.controllers      import mod_admin_auth      as admin_auth_module

from app.admin.mod_dashboard.controllers import mod_admin_dashboard as admin_dashboard_module
from app.admin.mod_home.controllers      import mod_admin_home      as admin_home_module
from app.admin.mod_media.controllers     import mod_admin_media     as admin_media_module
from app.admin.mod_tools.controllers     import mod_admin_tools     as admin_tools_module
from app.admin.mod_users.controllers     import mod_users           as admin_users_module

# Register blueprint(s)
app.register_blueprint( home_module )
app.register_blueprint( media_module )

app.register_blueprint( admin_acl_module )
app.register_blueprint( admin_auth_module )
app.register_blueprint( admin_dashboard_module )
app.register_blueprint( admin_home_module )
app.register_blueprint( admin_media_module )
app.register_blueprint( admin_tools_module )
app.register_blueprint( admin_users_module )

# End File: app/__init__.py
