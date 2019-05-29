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

			
			
			result_key = list(json_response)[2]
			print(result_key,'<-- this is result key in json resp')
			
			## save the whole obj as a var			
			result_val = list(json_response.values())[2]
			# print(type(result_val),'<-- type of result_val')

			print(type(result_val[3]),'<---result_val3 type')
			# for value in result_val[3]:
			# print(dict.values(result_val[3][0]),'<-- inside of dict.values')

			for k in result_val[3].keys():
				print(k,result_val[3][k])

			# enumerate	
			obj["name"]

			# print(result_val[3][5],'<---result_val5')
			# print(result_val[3][12],'<---result_val12')
			# for key in result_val.keys():
			# 	print(key,'<--key in result_val')
				
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







