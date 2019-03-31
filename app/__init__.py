# Import flask and template operators
from flask import Flask

from flask_jwt_extended import JWTManager

# Import SQLAlchemy
# from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Build the database:
# This will create the database file using SQLAlchemy
@app.before_first_request
def create_tables():
    db.create_all()


def buildIndex():
	page = """
			<h1>Welcome to the my tele app.</h1>
			<h3>Easily get the details of any phone number</h3>
			<a href="/auth"><button>SignIn</button></a>
	"""

	return page

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return 'Not Found', 404

@app.route('/', methods=['GET'])
def index():
	return buildIndex()

# Import a module / component using its blueprint handler variable (mod_auth)
from app.components.controllers import (
	mod_auth as auth_module,
	mod_search as search_module
)

# Register blueprint(s): and set its url prefix: app.url/auth
app.register_blueprint(auth_module, url_prefix='/auth')
app.register_blueprint(search_module, url_prefix='/search')
# app.register_blueprint(xyz_module)
# ..