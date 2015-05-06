# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from app.admin.mod_pages.models import Page

mod_home = Blueprint('home', __name__ )

# @todo: make this dynamic, duh
template_name = 'theme1'

@mod_home.route('/')
def index( ):
    """
        Main Index
    """
    return render_template( __get_template("index.html") )

@mod_home.route('/<uri>')
def cms_page( uri = None ):
    """
        CMS Routing 
    """
    page   = Page.query.filter( Page.uri == uri ).first()
    if not page:
        return redirect('/404')
    layout = "cms/%s.html" % page.layout
    return     render_template( __get_template( layout ), page = page )

@mod_home.route('/contact/')
def contact():
    data = {}
    return render_template( __get_template("contact.html"), d = data )

@mod_home.route('/menu/')
def menu():
    data = {}
    return render_template( __get_template( "menu.html" ), d = data )

@mod_home.route('/locations/')
def locations():
    data = {}
    return render_template( __get_template('locations.html'), d = data )

@mod_home.route('/404')
def error_404():
    return render_template('frontend/theme1/mod_home/404.html'), 404

def __get_template( template_file ):
    module_name   = 'mod_home'
    return 'frontend/%s/%s/%s' % ( template_name, module_name, template_file )

# End File: app/frontend/mod_home/controllers.py
