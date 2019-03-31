# Import flask dependencies
# from flask import Blueprint, request, render_template, \
#                   flash, g, session, redirect, url_for
from flask import Blueprint, request, redirect, url_for

from flask_restful import Resource, Api

# Import password / encryption helper tools
# from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db
from resources import SignIn, SignUp

# Import module models (i.e. User)
# from app.components.models import User

# Define the blueprint: 'auth'
mod_auth = Blueprint('auth', __name__)

auth_route = Api(mod_auth)

class Auth(Resource):
	def get(self):
		# redirect to SignIn route
		return redirect(url_for('auth.signin'))
	def post(self):
		pass

auth_route.add_resource(Auth, '/')
auth_route.add_resource(SignIn, '/signin/')
auth_route.add_resource(SignUp, '/signup')
