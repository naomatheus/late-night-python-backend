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
			location=[ 'json']
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
			restaurantsData = list(json_response.values())[2]

			for k, v in enumerate(restaurantsData):
				# restaurantData = {}
				print(k,v)
				print(v["name"])
				print(v["place_id"])
				print(v["vicinity"])
				restaurantData = dict(
						name=v["name"],
						place_id=v["place_id"],
						vicinity=v["vicinity"]
					)
				print(restaurantData)
			# restaurantData = restaurantsData["name"]["place_id"]["vicinity"]

			## create a dictionary with those properties and send over to the client

			## now change this route to look at the same k and v for all of the returned restaurant values 
			
		return restaurantData, 'this is restaurantData'

class Restaurant(Resource):
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
			location=[ 'json']
			)
		self.reqparse.add_argument(
			'place_id',
			required=False,
			help='No restaurant place_id provided',
			location=['json']
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

	@marshal_with(restaurant_fields)
	def post(self):
		args = self.reqparse_args()

		models.Restaurant.create(**args)


	### POST restaurants/place_id/comment
		##1.) when route hit - checks DB for existing restaurant 
		##2.) if no restaurant exists, create one
		##3.) create comments w/ referenced foreign field
		##4.) ...maybe .save() foreign field in restaurant table?

restaurants_api = Blueprint('resources.restaurants', __name__)
api = Api(restaurants_api)
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