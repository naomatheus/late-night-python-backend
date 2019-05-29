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
			# print(type(restaurantsData[3]),'<---restaurantsData3 type')

			# restaurantData = restaurantsData["name"]["place_id"]["vicinity"]
			# print(restaurantsData)

			for k, v in enumerate(restaurantsData):
				print(k,v)

			# for k in restaurantsData[3].keys():
			# 	print(k,restaurantsData[3][k])

			# # enumerate	
			# obj["name"]
				
			## only selectively return the fields that we need
			## place_id, address, name

			## create a dictionary with those properties and send over to the client

			
		return resp.json()


	@marshal_with(restaurant_fields)
	def post(self):
		args = self.reqparse_args()


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







