from flask import request

from flask_restful import Resource, reqparse

from app.components.models import User, Contact

from app import db
# from sqlalchemy.exc import IntegrityError


# req parser rules defined here to take care to parsing req body on POST req
# and to handle the errors for required fields

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('name', type = str, required = True, help = 'Name is required')
parser.add_argument('phone', type = int, required = True, help = 'Phone is required')
parser.add_argument('email', type = str)
parser.add_argument('registered_user', type = bool, dest = 'is_registered')
parser.add_argument('is_spam', type = bool)

# Set the route and accepted methods
class SignUp(Resource):

	def get(self):
		return { 'message': 'hello world, at SignUp' }

	def post(self):
		print 'Recieved SignUp request with body: {}'.format(request.get_json())

		args = parser.parse_args()

		print 'parsed data: {}'.format(args)

		# return { 'message': 'middle stop' }

		contact = Contact(
			phone = args['phone'],
			is_registered = args['is_registered'],
			is_spam = args['is_spam']
		)

		user = User(
			name = args['name'],
			email = args['email'],
			phone = args['phone']
		)

		user_creation_error = ''
		contact_creation_error = ''

		try:
			contact.save_to_db()
		except Exception as e:
			db.session().rollback()

			contact_creation_error = {
				'message': 'Error in saving data to contact {}'.format(e.message)
			}

		try:
			user.save_to_db()
		except Exception as e:
			db.session().rollback()

			user_creation_error = {
				'message': 'Error in saving data to user {}'.format(e.message)
			}

		# closing the db cursor to prevent leak
		db.session.close()

		if len(user_creation_error) > 0 or len(contact_creation_error) > 0:
			return {
				'status': 'error',
				'user': user_creation_error,
				'contact': contact_creation_error 
			}, 402

		return { 'message': 'signup successfull', 'body': args }, 201

