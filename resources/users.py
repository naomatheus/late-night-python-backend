import json
from flask import jsonify, Blueprint, abort, make_response
from flask_restful import (Resource, Api, reqparse, inputs, fields, marshal, marshal_with, url_for)
from flask_login import login_user, logout_user, login_required, current_user
import models

user_fields = {
	'username': fields.String,
	'password': fields.String,
	'email': fields.String
}

class UserList(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'username',
			required=True,
			help='No username provided',
			location=['form', 'json']
		)
		self.reqparse.add_argument(
			'password',
			required=True,
			help='No password provided',
			location=['form', 'json']
		)
		self.reqparse.add_argument(
			'email',
			required=True,
			help='No email provided',
			location=['form', 'json']
		)
		self.reqparse.add_argument(
			'verify_password',
			required=True,
			help='No pasword verification provided',
			location=['form', 'json']
			)
		super().__init__()


	def post(self):
		args = self.reqparse.parse_args()
		print((args), 'arguments to form body')
		if args['password'] == args['verify_password']:
			print(args, 'arguments to form body')
			user = models.User.create(**args)

			login_user(user)
			return marshal(user, user_fields), 201
		return make_response(
			json.dumps({
				'error': 'Password and password verificaiton do not match'
				}), 400)

class User(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'username',
			required=True,
			help='No username provided',
			location=['form', 'json']
		)
		self.reqparse.add_argument(
			'password',
			required=True,
			help='No password provided',
			location=['form', 'json']
		)
		self.reqparse.add_argument(
			'email',
			required=True,
			help='No email provided',
			location=['form', 'json']
		)
		self.reqparse.add_argument(
			'verify_password',
			required=True,
			help='No pasword verification provided',
			location=['form', 'json']
			)
		super().__init__()

	# @marshal_with(user_fields)
	def get(self,id):
		try: 
			user = models.User.get(models.User.id==id)
		except models.User.DoesNotExist:
			abort(404)
		else:
			return (user, 200)

	# @marshal_with(user_fields)
	def get(self,id):
		try:
			print(current_user,'<----- CURRENT USER ')
			logged_out_user = models.User.get(models.User.id==id)
			logout_user(logged_out_user)

		except models.User.DoesNotExist:
			abort(404)
		else:
			return (logged_out_user, 200)

	# def post(self, id):
	# 	args = self.reqparse.parse_args()
	# 	if args['password'] == args['verify_password']:
	# 		print(args, ' this is args')
	# 		user = models.User.create_user(**args)
	# 		login_user(user)





users_api = Blueprint('resources.users', __name__)

api = Api(users_api)

api.add_resource(
	UserList,
	'/registration',
)

api.add_resource(
	User,
	'/logout',
)


# api.add_resource(
# 	User,
# 	'/login',
# )
