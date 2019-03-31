from flask import request

from flask_restful import Resource, reqparse

from flask_jwt_extended import (
	create_access_token,
	create_refresh_token,
	jwt_refresh_token_required,
	get_jwt_identity,
	get_raw_jwt
)

from app.components.models import User

from app import db


parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('name', type = str, required = True, help = 'Name is required')
parser.add_argument('phone', type = int, required = True, help = 'Phone is required')


# Set the route and accepted methods
class SignIn(Resource):

	def get(self):
		return { 'message': 'hello world, at signin' }

	def post(self):
		print 'Recieved SignUp request with body: {}'.format(request.get_json())

		args = parser.parse_args()

		print 'parsed data: {}'.format(args)

		current_user = User.find_by_username_and_phone(args['name'], args['phone'])

		if not current_user:
			return {
				'message': 'User {} with phone {} doesn\'t exist'.format(args['name'], args['phone']),
				'status': 'error'
			}, 401

		print 'current_user {}'.format(current_user.name)
		access_token = create_access_token(identity = current_user.name)
		refresh_token = create_refresh_token(identity = current_user.name)

		return {
			'message': 'user login successfull',
			'status': 'success',
			'access_token': access_token,
			'refresh_token': refresh_token
		}
