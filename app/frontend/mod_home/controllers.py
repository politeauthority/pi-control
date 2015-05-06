# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

mod_home = Blueprint('home', __name__ )

template_name = 'theme1'

@mod_home.route('/')
def index( ):
    """
        Main Index
    """
    #app.log.info('hey')
    import subprocess
    p = subprocess.Popen(['ifconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    print out
    data = {
        'interfaces' : out
    }
    return render_template( __get_template("index.html"), **data )

@mod_home.route('/404')
def error_404():
    return render_template('frontend/theme1/mod_home/404.html'), 404

def __get_template( template_file ):
    module_name   = 'mod_home'
    return 'frontend/%s/%s/%s' % ( template_name, module_name, template_file )

# End File: app/frontend/mod_home/controllers.py
