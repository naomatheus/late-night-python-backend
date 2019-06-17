import json
from flask import jsonify, Blueprint, abort, make_response, request, g
from flask_restful import (Resource, Api, reqparse, inputs, fields, marshal, marshal_with, url_for)
from flask_login import login_user, logout_user, login_required, current_user
import models

user_fields = {
	'userName': fields.String,
	'password': fields.String,
	'email': fields.String
}

class UserList(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'userName',
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
		super().__init__()

	@marshal_with(user_fields)
	def post(self):
		args = self.reqparse.parse_args()
		print((args), 'arguments to form body')
		if args['password'] == args['password']:
			print(args, '<==== arguments to form body')
			user = models.User.create(**args)
			login_user(user)
			return marshal(user, user_fields), make_response(
				json.dumps({
					'data': user,
					'success': True
					}, 201)
			)
			# return marshal(user, user_fields), make_response(
			# 	json.dumps({
			# 		'success': True
			# 		}), 200)
		return make_response(
			json.dumps({
				'error': 'Password invalid'
				}), 400)

class User(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'userName',
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
			required=False,
			help='No email provided',
			location=['form', 'json']
		)
		super().__init__()

	@marshal_with(user_fields)
	def post(self):
		args = self.reqparse.parse_args()
		try:
			logged_in_user = models.User.get(models.User.userName==args.userName)
			print(logged_in_user)
		except models.User.DoesNotExist:
			abort(404)
		else:
			return (logged_in_user, 201)

	@marshal_with(user_fields)
	def get(self):
		try:
			print(current_user,'<----- CURRENT USER ')
			logged_out_user=current_user
			logout_user(logged_out_user)
		except models.User.DoesNotExist:
			abort(404)
		else:
			return (logged_out_user, 201)





users_api = Blueprint('resources.user', __name__)

api = Api(users_api)

api.add_resource(
	UserList,
	'/register/'
)

api.add_resource(
	User,
	'/logout/'
)

api.add_resource(
	User,
	'/login/',
	endpoint='auth'
)
