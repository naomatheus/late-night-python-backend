import json
from flask import jsonify, Blueprint, abort, make_response
from flask_restful import (Resource, Api, reqparse, inputs, fields, marshal, marshal_with, url_for)

import requests

from resources import restaurants

import models

import config

comment_fields = {
#### also need the foreign key here which is the place_id of the restaurants
	'commentBody': fields.String,
	'commentAuthor': fields.String
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
			'comment_author',
			required=False,
			help='No commentAuthor provided',
			location=['form', 'json']
			)
		super().__init__()

	@marshal_with(comment_fields)
	def post(self):
		args = self.reqparse.parse_args()
		print(args, '<===(req.body)')
		comment = models.Comment.create(**args)
		print(comment, '<===', type(comment))
		return (comment, 201)

comments_api = Blueprint('resources.comments', __name__)

api = Api(comments_api)

api.add_resource(
	Comment,
	'/comment/<int:id>'
)