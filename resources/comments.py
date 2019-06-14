import json
from flask import Flask, jsonify, Blueprint, abort, make_response, g
from flask_restful import (Resource, Api, reqparse, inputs, fields, marshal, marshal_with, url_for)

from flask_login import current_user

import requests

from resources import restaurants

import models

import config

comment_fields = {
#### also need the foreign key here which is the place_id of the restaurants
	'comment_body': fields.String,
	'comment_author_id': fields.String,
	'place_id': fields.String
}

class Comment(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'comment_body',
			required=False,
			help='No commentBody provided',
			location=['form', 'json']
			)
		self.reqparse.add_argument(
			'comment_author_id',
			required=False,
			help='No commentAuthor provided',
			location=['form', 'json']
			)
		super().__init__()

	# @marshal_with(comment_fields)
	def post(self):
		if g.user._get_current_object():
			print(g.user._get_current_object())
		args = self.reqparse.parse_args()
		print(args, '<===(req.body)')
		comment = models.Comment.create(comment_author=g.user._get_current_object(),**args)
		print(comment, '<===', type(comment))
		return (comment, 201)

	# @marshal_with(comment_fields)
	def put(self):
		args = self.reqparse.parse_args()
		print(args, '<===(req.body)')
		updated_comment = models.Comment.update(**args)
		print(updated_comment, '<===(req.body)', type(comment))
		return (comment, 201)

	# @marshal_with(comment_fields)
	def delete(self):
		comment_to_delete = models.Comment.delete()
		print(comment_to_delete, '<=== comment will be deleted', type(comment))
		return (comment_to_delete, 201)

comments_api = Blueprint('resources.comments', __name__)

api = Api(comments_api)

api.add_resource(
	Comment,
	'comment/<string:place_id>'
)