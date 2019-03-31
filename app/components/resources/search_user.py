from flask import request

from flask_restful import Resource

from app.components.models import User, Contact, get_all_users_by_name_or_phone

from app import db

class SearchUser(Resource):

	@staticmethod
	def getParsedData(resObject):
		parsedData = []
		for u, c in resObject:
			print parsedData.append(
				{
					'name': u.name,
					'email': u.email,
					'phone': c.phone,
					'is_registered': c.is_registered,
					'is_spam': c.is_spam		
				}
			)

		return parsedData


	@classmethod
	def search_user_by_username(self, name):
		result = get_all_users_by_name_or_phone(name, False)

		return self.getParsedData(result)

	@classmethod
	def search_user_by_phone(self, phone):
		result = get_all_users_by_name_or_phone(phone, True)

		return self.getParsedData(result)