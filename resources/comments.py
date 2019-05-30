# import json
# from flask import jsonify, Blueprint, abort, make_response
# from flask_restful import (Resource, Api, reqparse, inputs, fields, marshal, marshal_with, url_for)

# import requests

# from resources import restaurants

# import models

# import config

# comment_fields = {
# #### also need the foreign key here which is the place_id of the restaurants
# 	'commentBody': fields.String,
# 	'commentAuthor': fields.String
# }

# class Comment(Resource):
# 	def __init__(self):
# 		self.reqparse = reqparse.RequestParser()
# 		self.reqparse.add_argument(
# 			'commentBody',
# 			required=False,
# 			help='No commentBody provided',
# 			location=['form', 'json']
# 			)
# 		self.reqparse.add_argument(
# 			'commentAuthor',
# 			required=False,
# 			help='No commentAuthor provided',
# 			location=['form', 'json']
# 			)

# 		super().__init__()


