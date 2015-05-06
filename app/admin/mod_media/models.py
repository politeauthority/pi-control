"""
    MEDIA - MODEL
"""
from flask import current_app as app
from app import db
from app.admin.mod_users.models import User

class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

class Media(Base):

    __tablename__ = 'media'

    name        = db.Column(db.String(256),  nullable=False)
    file_name   = db.Column(db.String(256),  nullable=False)
    file_path   = db.Column(db.String(256),  nullable=False)
    file_size   = db.Column(db.Integer,      nullable=False)
    file_ext    = db.Column(db.String(10),   nullable=False)
    file_type   = db.Column(db.String(25),   nullable=False)
    description = db.Column(db.String(256) )
    created_by  = db.Column(db.Integer,      nullable=False)
    modified_by = db.Column(db.Integer,      nullable=False)

    def __init__(self, id = None, file_name = None ):
        if id:
            self.id = id
            m = self.query.filter( Media.id == id ).first()
            if m:
                self.__build_obj__( m )
        elif file_name:
            self.file_name = file_name
            m = self.query.filter( Media.file_name == file_name ).first()
            if m:
                self.__build_obj__( m )

    def __repr__(self):
        return '<Media %r, %r>' % (self.name, self.id)

    def __build_obj__( self, m ):
        self.id            = m.id
        self.name          = m.name
        self.file_name     = m.file_name
        self.file_path     = m.file_path
        self.file_size     = m.file_size
        self.file_ext      = m.file_ext
        self.file_type     = m.file_type
        self.description   = m.description
        self.created_by    = m.created_by
        self.modified_by   = m.modified_by
        self.date_created  = m.date_created
        self.date_modified = m.date_modified
        self.creator       = User( m.created_by )
        app.logger.debug( 'This is the creator %s' % self.creator )

    def save( self ):
        if self.id == None:
            new_media = self
            db.session.add( new_media )
        db.session.commit()

    def delete( self ):
        if self.id:
            delete_media = self.query.filter( Media.id == self.id ).first()
            if not delete_media:
                return False
            db.session.delete( delete_media )
            db.session.commit()
            return True
        return False

# End File: app/admin/mod_media/models.py
