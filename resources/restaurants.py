# import app from resources
import json
from flask import jsonify, Blueprint, abort, make_response
from flask_restful import (Resource, Api, reqparse, inputs, fields, marshal, marshal_with, url_for)

import requests



import models

import config

restaurant_fields = {
	'name': fields.String,
	'address': fields.String,
	'place_id': fields.String
}

comment_fields = {
#### also need the foreign key here which is the user_id of the restaurants
	'place_id': fields.Integer,
	'commentBody': fields.String,
	'commentAuthor': fields.Integer
}

class Comment(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument(
			'commentBody',
			required=False,
			help='No comment body provided',
			location=['form', 'json']
			)
		self.reqparse.add_argument(
			'commentAuthor',
			required=False,
			help='No comment author provided',
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

	@marshal_with(restaurant_fields)
	def get(self):
		resp = requests.get(config.API_URL + config.API_KEY)
		json_response = resp.json()
		if resp.status_code != 200:
			raise ApiError('GET /restaurants/{}'.format(resp.status_code))
		else:
			getRestaurantsResponse = resp.json()			
			print(type(json_response),'<-- this is the type of the json_response')
			## save the whole obj as a var			
			restaurantsData = list(json_response.values())[2]
			allRestaurants = []
			restaurantData = {}
			for k, v in enumerate(restaurantsData):
				print(k,v,'==================================================')
				print(v["name"])
				print(v["place_id"])
				print(v["vicinity"])
				restaurantData = dict(
						name=v["name"],
						place_id=v["place_id"],
						address=v["vicinity"]
					)
				allRestaurants.append(restaurantData)
				# print(restaurantsData)
				# restaurantData = restaurantsData[4][7][15]

			## create a dictionary with those properties and send over to the client

			## now change this route to look at the same k and v for all of the returned restaurant values 
			
		# return getRestaurantsResponse
		print('START')
		print(allRestaurants,'==============================')
		return allRestaurants
		print('END')

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

	@marshal_with(restaurant_fields)
	def post(self, place_id):
		# print(reqparse.parse_args)
		args = self.reqparse.parse_args()
		# foundRestaurant = models.Restaurant.select(**args)
		# print(foundRestaurant)
		# print(g.user._get_current_object())
		# if foundRestaurant:
		print(args, '<==== args (req.body')
		restaurant = models.Restaurant.create(**args)
		print(restaurant, '<===', type(restaurant))
		# models.Restaurant.create(**args)
		# elif foundRestaurant:
		# 	if g.user._get_current_object():
		# 		if foundRestaurant.place_id == place_id:
		return (restaurant, 201)

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

# comments_api = Blueprint('resources.comments', __name__)
	
restaurants_api = Blueprint('resources.restaurants', __name__)

api = Api(restaurants_api)
# comment_api = Api(comments_api)
api.add_resource(
	RestaurantList,
	'/'
)
api.add_resource(
    Restaurant,
    '/restaurants/<string:place_id>'
)
# comment_api.add_resource(
# 	Comment,
# 	'<string:place_id>/comment',
# 	endpoint='comment'
# 	)