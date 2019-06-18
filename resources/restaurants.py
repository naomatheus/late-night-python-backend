import json
from flask import jsonify, Blueprint, abort, make_response, request
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
    'place_id': fields.String,
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
            restaurantsData = list(json_response.values())[2]
            ## save the whole obj as a var
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
            
        print('START==============================')
        print(allRestaurants)
        print('END==============================')
        return allRestaurants

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
    def get(self):   
        searchTerm = request.args.get('searchTerm')
        url = (config.GEO_LOC_API_URL + searchTerm + config.GEO_LOC_API_FIELDS + config.API_KEY)
        print(url,'<--- this is the URL I will access')
        resp = requests.get(url)
        print(resp,'<--- this is response in the restaurant API call w/ geolocation')
        if resp.status_code != 200:
            raise ApiError('GET /restaurants/{}'.format(resp.status_code))
        else:
            oneRestaurant = resp.json()  
        return ({'data':oneRestaurant})
        
class RestaurantComment(Resource):
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
    # @marshal_with(restaurant_fields)
    def post(self, place_id):
        args = self.reqparse.parse_args()
        foundRestaurant = models.Restaurant.select(**args)
        print(foundRestaurant)
        print(g.user._get_current_object())
        if foundRestaurant:
            print(args, '<==== args (req.body')
            restaurant = models.Restaurant.create(**args)
            print(restaurant, '<===', type(restaurant))
            models.Restaurant.create(**args)
        elif not foundRestaurant:
            if g.user._get_current_object():
                if foundRestaurant.place_id==place_id:
                    return (restaurant, 201)
    ### POST restaurants/place_id/comment
        ##1.) when route hit - checks DB for existing restaurant 
        ##2.) if no restaurant exists, create one
        ##3.) create comments w/ referenced foreign field
        ##4.) ...maybe .save() foreign field in restaurant table?

    
restaurants_api = Blueprint('resources.restaurants', __name__)
api = Api(restaurants_api)

api.add_resource(
    RestaurantList,
    '/'
)
api.add_resource(
    Restaurant,
    '/nearby'
)

api.add_resource(
	RestaurantComment,
	'/<place_id>/comments'
)