# Import flask dependencies
# from flask import Blueprint, request, render_template, \
#                   flash, g, session, redirect, url_for
from flask import Blueprint, request, redirect, url_for, make_response

from flask_restful import Resource, Api, reqparse

from flask_jwt_extended import jwt_required

# Import password / encryption helper tools
# from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db
from resources import SignIn, SignUp, SearchUser

# Import module models (i.e. User)
# from app.components.models import User

# Define the blueprint: 'auth'
mod_auth = Blueprint('auth', __name__)
mod_search = Blueprint('search', __name__)

auth_route = Api(mod_auth)
search_route = Api(mod_search)

class Auth(Resource):
	def get(self):
		# redirect to SignIn route
		return redirect(url_for('auth.signin'))
	def post(self):
		pass

class SearchUserIndex(Resource):

	parser = reqparse.RequestParser(bundle_errors=True)
	parser.add_argument('name', type = str, help = 'Name is required')
	parser.add_argument('phone', type = int, help = 'Phone is required')
		

	def get(self):
		response = make_response('<h1>Search Page</h1>')
		response.headers['content-type'] = 'text/html'

		return response

	@jwt_required
	def post(self):
		print 'search query, {}'.format(request.get_json())

		args = self.parser.parse_args()

		print 'parsed data: {}'.format(args)

		if args['name'] is None and args['phone'] is None:
			return {
				'message': 'At least name or phone key is required',
				'status': 'error'
			}, 403

		searchObj = SearchUser()

		searchList = []

		if args['name'] is not None:
			# search by name
			print 'searching by name -> {}'.format(args['name'])

			searchList = searchObj.search_user_by_username(args['name'])
		elif args['phone'] is not None:
			# search by phone
			print 'searching by phone -> {}'.format(args['phone'])
			searchList = searchObj.search_user_by_phone(args['phone'])

		return {
			'message': 'search results',
			'status': 'success',
			'data': searchList
		}

auth_route.add_resource(Auth, '/')
auth_route.add_resource(SignIn, '/signin')
auth_route.add_resource(SignUp, '/signup')

search_route.add_resource(SearchUserIndex, '/')
