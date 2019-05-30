# import app from resources
import json
from flask import jsonify, Blueprint, abort, make_response
from flask_restful import (Resource, Api, reqparse, inputs, fields, marshal, marshal_with, url_for)

import requests

from resources import comments

import models

import config

restaurant_fields = {
	'name': fields.String,
	'address': fields.String,
	'place_id': fields.String
}

comment_fields = {
#### also need the foreign key here which is the place_id of the restaurants
	'place_id': fields.Integer,
	'comment_body': fields.String,
	'comment_author': fields.Integer
}

class Comment(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'comment_body',
			required=False,
			help='No comment_body provided',
			location=['form', 'json']
			)
		self.reqparse.add_argument(
			'comment_author',
			required=False,
			help='No comment_author provided',
			location=['form', 'json']
			)		
		super().__init__()


class RestaurantList(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'name',
			required=False,
			help='No restaurant name provided',
			location=['json']
			)
		self.reqparse.add_argument(
			'address',
			required=False,
			help='No restaurant address provided',
			location=['json']
			)
		self.reqparse.add_argument(
			'place_id',
			required=False,
			help='No restaurant place_id provided',
			location=['json']
			)
		super().__init__()

	def get(self):
		resp = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=41.8781,-87.6298&radius=5000&type=restaurant&keyword=open&keyword=late&key=AIzaSyDchPWjgowvaycrHzTZj44OEMBLdmt6584')

		if resp.status_code != 200:
			raise ApiError('GET /restaurants/{}'.format(resp.status_code))
		else:	
			json_response = resp.json()
			

			print(type(json_response),'<-- this is the type of the json_response')
			
			## save the whole obj as a var			
			# restaurantsData = list(json_response.values())[2]

			# for k, v in enumerate(restaurantsData):
			# 	# restaurantData = {}
			# 	print(k,v)
			# 	print(v["name"])
			# 	print(v["place_id"])
			# 	print(v["vicinity"])
			# 	restaurantData = dict(
			# 			name=v["name"],
			# 			place_id=v["place_id"],
			# 			vicinity=v["vicinity"]
			# 		)
			# 	print(restaurantData)
			# restaurantData = restaurantsData["name"]["place_id"]["vicinity"]

			## create a dictionary with those properties and send over to the client

			## now change this route to look at the same k and v for all of the returned restaurant values 
			
		return json_response, 'this is restaurantData'

class Restaurant(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'name',
			required=False,
			help='No restaurant name provided',
			location=['form', 'json']
			)

		self.reqparse.add_argument(
			'address',
			required=False,
			help='No restaurant address provided',
			location=['form', 'json']
			)

		self.reqparse.add_argument(
			'place_id',
			required=False,
			help='No restaurant place_id provided',
			location=['form', 'json']
			)

		super().__init__()

	def get(self, place_id):
		resp = requests.get('https://maps.googleapis.com/maps/api/place/details/json?placeid=' + place_id + '&fields=name,formatted_address,place_id&key=AIzaSyDchPWjgowvaycrHzTZj44OEMBLdmt6584')
		print(resp,'<-- this is response in the second get restaurant call')

		if resp.status_code != 200:
			raise ApiError('GET /restaurants/{}'.format(resp.status_code))

		else:
			oneRestaurant = resp.json()
		print(oneRestaurant,'<-- this is one restaurant')
		
		return oneRestaurant

	# @app.route('/<string:place_id>/comment',methods=['GET'])
	@marshal_with(comment_fields)
	@marshal_with(restaurant_fields)

	def post(self, place_id):
		_json = request.json
		_name=_json.name
		_address=_json.address
		_place_id = _json.place_id
		_comment_body=_json.comment_body
		_comment_author=_json.user_id
		print(reqparse.parse_args)
		print("HITTING THIS BLOCK? a")
		args = self.reqparse.parse_args()
		print("HITTING THIS BLOCK? b")
		foundRestaurant = models.Restaurant.select(**args)
		print("HITTING THIS BLOCK? c")
		print(foundRestaurant)
		print("HITTING THIS BLOCK? d")
		print(g.user._get_current_object())
		print("HITTING THIS BLOCK? e")
		if  foundRestaurant:
			print(args, '<==== args (req.body')
			restaurant = models.Restaurant.create(**args)
			print(restaurant, '<===', type(restaurant))
			models.Restaurant.create(**args)
		elif foundRestaurant:
			print("HITTING THIS BLOCK? f")
			if g.user._get_current_object():
				comment = models.Comment.create(**args)
		if foundRestaurant.place_id == place_id:
			print("HITTING THIS BLOCK? g")
			comment.save()
			print("HITTING THIS BLOCK? h")
		return (restaurant, comment, 201)

	### POST restaurants/place_id/comment
		##1.) when route hit - checks DB for existing restaurant 
		##2.) if no restaurant exists, create one
		##3.) create comments w/ referenced foreign field
		##4.) ...maybe .save() foreign field in restaurant table?


# class Comment(Resource):
# 	def __init__(self):
# 		self.reqparse = reqparse.RequestParser()
# 		self.reqparse.add_argument(
# 			'comment_body',
# 			required=False,
# 			help='No comment_body provided',
# 			location=['form', 'json']
# 			)
# 		self.reqparse.add_argument(
# 			'comment_author',
# 			required=False,
# 			help='No comment_author provided',
# 			location=['form', 'json']
# 			)		
# 		super().__init__()

comments_api = Blueprint('resources.comments', __name__)
	
restaurants_api = Blueprint('resources.restaurants', __name__)

api = Api(restaurants_api)
comment_api = Api(comments_api)
api.add_resource(
	RestaurantList,
	'/restaurants',
	endpoint='restaurants'
)
api.add_resource(
    Restaurant,
    '/restaurant/<string:place_id>',
    endpoint='restaurant'
)
comment_api.add_resource(
	Comment,
	'<string:place_id>/comment',
	endpoint='comment'
	)