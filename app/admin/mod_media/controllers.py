"""
	ADMIN MEDIA - CONTROLLER
"""
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect

from app.admin.mod_media.models import Media
from app.helpers.decorators import *
from app.helpers.upload import Upload

mod_admin_media = Blueprint('AdminMedia', __name__, url_prefix='/admin/media')

@mod_admin_media.route('/')
@requires_auth
def index():
	media = Media.query.order_by( Media.date_modified.desc() ).all()
	# media = Media.query.all()
	return render_template( 'admin/mod_media/roster.html', media = media )

@mod_admin_media.route('/info/<media_id>')
@requires_auth
def info( media_id ):
	media = Media( media_id )
	return render_template( 'admin/mod_media/info.html', media = media )

@mod_admin_media.route('/create/', methods=['GET', 'POST'] )
@requires_auth
def create():
	if request.method == "POST":
		phile = request.files['media_file']
		uploaded = Upload().file( phile, store_dir = 'media' )
		if uploaded:
			media = Media( file_name = uploaded['file_name'] )
			if request.form['media_name'] != '':
				media_name = request.form['media_name']
			else:
				media_name = uploaded['file_name_orig']		
			media.name             = media_name
			media.file_path        = uploaded['relative_path']
			media.file_size        = uploaded['file_size']
			media.file_ext         = uploaded['file_ext']
			media.file_type        = uploaded['file_type']
			media.description      = request.form['media_description']
			media.created_by       = session['user_id']
			media.modified_by      = session['user_id']
			media.save()
			return redirect( '/admin/media/' )
	return render_template( 'admin/mod_media/create.html')

@mod_admin_media.route('/edit/<media_id>', methods=['GET', 'POST'] )
@requires_auth
def edit( media_id ):
	media = Media.query.filter( Media.id == media_id ).first()
	if request.method == "POST":
		media.name        = request.form['media_name']
		media.description = request.form['media_description']
		media.modified_by = session['user_id']
		media.save()
		return redirect( '/admin/media/info/' + media_id )
	return render_template('admin/mod_media/edit.html', media = media)

@mod_admin_media.route('/delete/<media_id>')
@requires_auth
def delete( media_id ):
	Media( media_id ).delete()
	return redirect('/admin/media')

# End File: app/admin/mod_media/controllers.py
