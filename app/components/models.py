# Import the database object (db) from the main application module
from app import db

# Define a base model for other database tables to inherit
# class Base(db.Model):

#     __abstract__  = True

#     id            = db.Column(db.Integer, primary_key=True)
#     # date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
#     # date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
#     #                                        onupdate=db.func.current_timestamp())

# Define a User model
class Contact(db.Model):

    __tablename__    = 'contacts'

    # Phone number primary key
    phone            = db.Column(db.String(10),  nullable = False, primary_key = True)
    is_registered    = db.Column(db.Boolean,  unique = False, default = False)
    is_spam          = db.Column(db.Boolean,  unique = False, default = False)

    # defining the one-to-many relationship to user table
    children         = db.relationship("User", back_populates = "parent")

    # New instance instantiation procedure
    def __init__(self, phone, is_registered, is_spam):

        self.phone            = phone
        self.is_registered    = is_registered
        self.is_spam          = is_spam

    def __repr__(self):
        return '<User %r>' % (self.phone)





class User(db.Model):

    __tablename__    = 'users'

    name             = db.Column(db.String(128), nullable = False)
    email            = db.Column(db.String(128, nullable = True))

    # defining phone as foreign key to established relationship with Contact table
    phone            = db.Column(db.String(10), db.ForeignKey('parent.phone'))

    # providing back reference
    parent           = db.relationship("Contact", back_populates = "children")

    def __init__(self, name, email, phone):

        self.name    = name
        self.email   = email
        self.phone   = phone

    def __repr__(self):
        return '<User %r>' % (self.name)
