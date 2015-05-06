# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

class ChangeLog(Base):

    __tablename__ = 'log_change'

    # User Name
    user_id       = db.Column(db.Integer(10) , nullable=False)
    entity_type   = db.Column(db.String(128),  nullable=False)
    change        = db.Column(db.String(128),  nullable=False)
    before_change = db.Column(db.String(128),  nullable=False)
    afgter_change = db.Column(db.String(128),  nullable=False)

    # Authorisation Data: role & status
    # status   = db.Column(db.SmallInteger, nullable=False)

    # New instance instantiation procedure
    def __init__(self, id = None, name = None ):
        if id:
            u = self.query.filter( User.id == id ).first()
            if u:
                self.id     = int( id )
                self.name   = u.name
                self.email  = u.email
        elif name:
            self.name = name

    def __repr__(self):
        return '<Change %r, %r>' % (self.name, self.id)

    def save(self):
        if self.id == None:
            new_user = self
            db.session.add( new_user )
            db.session.commit()

    def delete( self ):
        if self.id:
            delete_user = self.query.filter( User.id == self.id ).first()
            if not delete_user:
                return False
            db.session.delete( delete_user )
            db.session.commit()
            return True
        return False

# End File: app/admin/mod_changelog/models.py
