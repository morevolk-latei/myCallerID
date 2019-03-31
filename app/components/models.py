# Import the database object (db) from the main application module
from app import db

from sqlalchemy import and_, or_, not_, inspect

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
    phone            = db.Column(db.String(10),  nullable = False, primary_key = True, index = True)
    is_registered    = db.Column(db.Boolean,  unique = False, default = False)
    is_spam          = db.Column(db.Boolean,  unique = False, default = False)

    # defining the one-to-many relationship to user table
    user         = db.relationship("User", cascade="all, delete-orphan", backref = "contacts")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

    @classmethod
    def get_all_users_by_phone(self, phone):
        return self.query.join(User).filter(self.phone.like('%{}%'.format(phone))).all()

    # New instance instantiation procedure
    def __init__(self, phone, is_registered = False, is_spam = False):

        self.phone            = phone
        self.is_registered    = is_registered
        self.is_spam          = is_spam

    def __repr__(self):
        return '<User %r>' % (self.phone)





class User(db.Model):

    __tablename__    = 'users'

    id               = db.Column(db.Integer, primary_key = True)
    name             = db.Column(db.String(128), nullable = False, index = True, unique = True)
    email            = db.Column(db.String(128), nullable = True, default = None)

    # defining phone as foreign key to established relationship with Contact table
    phone            = db.Column(db.String(10), db.ForeignKey('contacts.phone'))

    # providing back reference
    contact           = db.relationship("Contact", backref = "users")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }


    @classmethod
    def find_by_username(self, username):
       return self.query.filter_by(name = username).first()


    @classmethod
    def find_by_username_and_phone(self, username, phone):
       return self.query.filter(
            and_(
                self.name.like(username),
                self.phone.like(phone)
            )
        ).first()

    @classmethod
    def get_all_users_by_name(self, name):
        return self.query.join(Contact).filter(self.name.like('%{}%'.format(name))).all()

    def __init__(self, name, email, phone):

        self.name    = name
        self.email   = email
        self.phone   = phone

    def __repr__(self):
        return '<User %r>' % (self.name)


def get_all_users_by_name_or_phone(query, isPhone):
    # query = db.session.query(User).join(Contact).filter(User.name.like('%{}%'.format(name))).all()
    query = db.session.query(User, Contact).filter(User.phone == Contact.phone).filter(
            or_(
                User.name.like('%{}%'.format(query)),
                User.phone.like('%{}%'.format(query))
            )
        ).all()
    print query

    return query