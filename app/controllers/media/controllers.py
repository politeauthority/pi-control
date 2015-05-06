import os
from  hashlib import md5
from PIL import Image

from flask import Blueprint, send_file, redirect, request
from flask import current_app as app

media = Blueprint('Media', __name__, url_prefix='/media')

@media.route('/<path:varargs>')
def index( varargs = None ):
  args = varargs.split('/')

  if args[0] =='uploads' and args[1] == 'media' and len( args[2] ) == 4 and len( args[3] ) == 2:
    file_path = os.path.join(
      app.config['UPLOAD_DIR'],
      args[1],
      args[2],
      args[3],
      args[4]
    )
    adjustments = __find_img_args( args )
    cache_key = image_cache_key( file_path, adjustments )
    cache_location = os.path.join( app.config['CACHE_DIR'], cache_key )
    if os.path.exists( cache_location ):
        return send_file( str( cache_location ), mimetype="image/jpg" )
    else:
        __run_image_adjustments( file_path, adjustments )
        return send_file( str( cache_location ), mimetype="image/jpg" )
  else:
    return 'fart'

def image_cache_key( file_path, adjustments ):
  return md5( file_path + str( adjustments ) ).hexdigest()

def __find_img_args( args ):
    image_adj = {}
    c = 0
    for arg in args:
        if arg == 'crop':
            image_adj['crop'] = args[c+1].split(',')
        if arg == 'maxwidth':
            image_adj['maxwidth'] = args[c+1].split(',')            
        c += 1
        if arg[0] == 'v' and arg[1:].isdigit():
            image_adj['version'] = arg[1:]
    return image_adj

def __run_image_adjustments( file_path, adj ):
    try:
      image = Image.open( file_path )
    except IOError, e:
      app.logger.warning( 'Image not found on disk: %s' % request.url )
      image = Image.open( os.path.join( app.config['BASE_DIR'], 'app/static/media/placeholder.jpg' ) )
    if 'crop' in adj:
        image.thumbnail( ( int( adj['crop'][0] ), int( adj['crop'][1] ) ), Image.ANTIALIAS )
    elif 'maxwidth' in adj:
        image.thumbnail( ( int( adj['maxwidth'][0] ), int( adj['maxwidth'][1] ) ), Image.ANTIALIAS )        
    cache_key  = image_cache_key( file_path, adj )
    cache_file = os.path.join( app.config['CACHE_DIR'], cache_key ) 
    image.save( cache_file, "JPEG")
    return cache_file

# End File: app/media/controllers.py 
