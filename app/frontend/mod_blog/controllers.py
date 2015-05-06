"""
	BLOG - CONTROLLER
"""
from flask import current_app as app
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
from app.admin.mod_blog.models import Post, PostTag, PostCategory
from app.helpers.pagination import Pagination

from datetime import datetime

mod_blog = Blueprint('blog', __name__, url_prefix='/blog' )

# @todo: make this dynamic, duh
template_name = 'theme1'

@mod_blog.route('/', defaults={'page': 1})
@mod_blog.route('/page/<int:page>/')
def index( page ):
  per_page = 5
  qry_args = (
    Post.status == 'published', 
    Post.date_published <= datetime.now(),
  )
  data = {}
  data['posts_count'] = Post().query.filter( *qry_args ).count()
  if page == 1:
    data['posts']  = Post().query.filter( *qry_args ).order_by( Post.date_published.desc() ).limit( per_page )
  else:
    data['posts']  = Post().query.filter( *qry_args ).order_by( Post.date_published.desc() ).limit( per_page ).offset( ( ( page * per_page ) - per_page ) )
  data['pagination']  = Pagination( page, per_page, data['posts_count'] )    
  return render_template( __get_template("index.html"), **data )

@mod_blog.route('/<int:year>/<month>/<slug>')
def single( year, month, slug ):
  uri = "%s/%s/%s" % ( year, month, slug )
  qry_args = (
    Post.status == 'published',
    Post.date_published <= datetime.now(),
    Post.uri == uri
  )
  data = {}
  data['post'] = Post.query.filter( *qry_args ).first()
  if not data['post']:
    return redirect('/404')
  return render_template( __get_template('single.html'), **data )

@mod_blog.route('/tag/<slug>/', defaults={'page': 1})
@mod_blog.route('/tag/<slug>/page/<int:page>/')
def tag( slug, page ):
  per_page = 5
  tag = PostTag.query.filter( PostTag.slug == slug ).first()
  if not tag:
    return redirect('/404/')
  app.logger.debug(tag)
  qry_args = (
    Post.status == 'published', 
    Post.date_published <= datetime.now(),
    Post.tags.like( "%" + str(tag.id) + ",%" )
  )
  data = {}
  data['posts_count'] = Post().query.filter( *qry_args ).count()
  if data['posts_count'] > 0:
    if page == 1:
      data['posts']  = Post().query.filter( *qry_args ).order_by( Post.date_published.desc() ).limit( per_page )
    else:
      data['posts']  = Post().query.filter( *qry_args ).order_by( Post.date_published.desc() ).limit( per_page ).offset( ( ( page * per_page ) - per_page ) )
  else:
    data['posts'] = []
  data['pagination']  = Pagination( page, per_page, data['posts_count'] )    
  return render_template( __get_template("index.html"), **data )

@mod_blog.route('/category/<slug>/', defaults={'page': 1})
@mod_blog.route('/category/<slug>/page/<int:page>/')
def category( slug, page ):
  per_page = 5
  cat = PostCategory.query.filter( PostCategory.slug == slug ).first()
  if not cat:
    return redirect('/404/')
  app.logger.debug(cat)
  qry_args = (
    Post.status == 'published', 
    Post.date_published <= datetime.now(),
    Post.categories.like( "%" + str(cat.id) + ",%" )
  )
  data = {}
  data['posts_count'] = Post().query.filter( *qry_args ).count()
  if page == 1:
    data['posts']  = Post().query.filter( *qry_args ).order_by( Post.date_published.desc() ).limit( per_page )
  else:
    data['posts']  = Post().query.filter( *qry_args ).order_by( Post.date_published.desc() ).limit( per_page ).offset( ( ( page * per_page ) - per_page ) )
  data['pagination']  = Pagination( page, per_page, data['posts_count'] )    
  return render_template( __get_template("index.html"), **data )

def __get_template( template_file ):
    module_name   = 'mod_blog'
    return 'frontend/%s/%s/%s' % ( template_name, module_name, template_file )

# End File: app/frontend/mod_blog/controllers.py
