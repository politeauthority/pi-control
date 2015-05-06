"""
    Uploader
"""

import os
import datetime
from werkzeug import secure_filename

from flask import flash
from flask import current_app as app

class Upload(object):

    def file( self, phile, store_dir = None ):
        self.phile      = phile
        self.o_phile    = phile.filename
        self.phile_name = phile.filename
        self.ext        = self.allowed_file()
        self.extra_dir  = store_dir
        if self.ext:
            self.phile_name = secure_filename( phile.filename )
            self.build_phile_path()
            if os.path.exists( os.path.join( self.phile_path, self.phile_name ) ):
                self.handle_file_collision( )
            save_path = os.path.join( self.phile_path, self.phile_name )
            phile.save( save_path )
            return self.set_upload_info()
        else:
            return False

    def allowed_file( self ):
        ext = self.phile_name[  self.phile_name.rfind( '.' ) + 1 : ].lower()
        if ext in app.config['ALLOWED_EXTENSIONS']:
            if ext == 'jpeg':
                ext = 'jpg'
            return ext
        else:
            return False

    def build_phile_path( self ):
        #@todo: this could probably be more secure
        self.phile_path = os.path.join( app.config['UPLOAD_DIR'],
            self.extra_dir,
            str( datetime.datetime.now().year ),
            '%02d' % datetime.datetime.now().month  )
        if not os.path.exists( self.phile_path ):
            os.makedirs( self.phile_path )

    def handle_file_collision( self ):
        g_phile_name = self.phile_name
        increment_section = g_phile_name[ g_phile_name.rfind('_') + 1 : g_phile_name.rfind( '.' + self.ext ) ]
        if '_' in g_phile_name and increment_section.isdigit():
            new_preffix = g_phile_name[ : g_phile_name.rfind( '_%s.%s' % ( increment_section, self.ext) ) ]
            new_file_name = "%s_%s.%s" % ( new_preffix, str( int( increment_section ) + 1 ), self.ext )
        else:
            new_file_name = g_phile_name[  : g_phile_name.rfind( '.' + self.ext ) ]
            new_file_name = '%s_1.%s' % ( new_file_name, self.ext )
        self.phile_name = new_file_name    
        if os.path.exists( os.path.join( self.phile_path, self.phile_name ) ):
            self.handle_file_collision()
        else:
            return True

    def set_upload_info( self ):
        full_path = os.path.join( self.phile_path, self.phile_name )
        relative_path = full_path.replace( app.config['BASE_DIR'], '' )
        if relative_path[0] == '/':
            relative_path = relative_path[1:]
        info = {
            'relative_path' : relative_path,
            'file_name_orig': self.o_phile,
            'full_path'     : full_path,
            'file_name'     : self.phile_name,
            'file_size'     : os.path.getsize( full_path ),
            'file_ext'      : self.ext,
            'file_type'     : 'image/%s' % self.ext
        }
        return info

# End File: app/helpers/uploader.py
