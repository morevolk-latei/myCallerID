from flask import request

from flask_restful import Resource


# Set the route and accepted methods
class SignIn(Resource):

	def get(self):
		return { 'message': 'hello world, at signin' }

	def post(self):
		req_body = request.get_json()
		return { 'message': 'post signIn', body: req_body }, 201

