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
		resp = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=41.8781,-87.6298&radius=5000&type=restaurant&keyword=open&keyword=late&key=AIzaSyCbQ8Y7CHZUWrnEGUCqC8fNR4Kw1dfk5AE')
		if resp.status_code != 200:
			raise ApiError('GET /restaurants/{}'.format(resp.status_code))
		for restaurant_fields in resp.json():
			print(restaurant_fields)
			new_restaurants = [marshal(restaurant, restaurant_fields) for restaurant in models.Restaurant.select()]
		return new_restaurants


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
# api.add_resource(
# 	RestaurantList,
# 	'/restaurants',
# 	endpoint='restaurants'
# )







