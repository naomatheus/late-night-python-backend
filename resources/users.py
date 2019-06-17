import json
from flask import jsonify, Blueprint, abort, make_response, request, g
from flask_restful import (Resource, Api, reqparse, inputs, fields, marshal, marshal_with, url_for)
from flask_login import login_user, logout_user, login_required, current_user
import models

user_fields = {
    'userName': fields.String,
    'password': fields.String,
    'email': fields.String
}

class UserList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'userName',
            required=True,
            help='No username provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'email',
            required=True,
            help='No email provided',
            location=['form', 'json']
        )
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        print((args), 'arguments to form body')
        if args['password'] == args['password']:
            print(args, '<==== arguments to form body')
            user = models.User.create_users(**args)
            login_user(user)
            return ({
            	'data': user,
            	'registered': True
            	})      

class GetUserData(Resource):
    def get(self):
        return('Restaurants')

class User(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'userName',
            required=True,
            help='No username provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'email',
            required=False,
            help='No email provided',
            location=['form', 'json']
        )
        super().__init__()


    def post(self):
        args = self.reqparse.parse_args()
        try:
            logged_in_user = models.User.get(models.User.userName==args.userName)
            print(logged_in_user.userName)
        except models.User.DoesNotExist:
            abort(404)
        else:
            user = marshal(logged_in_user, user_fields)
            return ({
                    'data': user,
                    'success': True
                    })

    def get(self):
        try:
            print(current_user,'<----- CURRENT USER ')
            logged_out_user=current_user
            logout_user()
        except models.User.DoesNotExist:
            abort(404)
        else:
            return ({
            	'data': current_user,
            	'loggedout': True
            	})


# ///this route returns all comments made by a user's session///
# router.get('/usercomments', async (req, res, next) => {
#     try{
#         if (req.session.logged === true){

#             const foundUser = await User.findOne({userName: req.session.userName})
#             if (foundUser){
#                 const foundRestaurants = await Restaurant.find({userName: req.session.userName}).populate('comments');
#                 const foundComments = await Comment.find({commentAuthor: req.session.userName})
#                 res.json({
#                     status: 200,
#                     data: foundRestaurants, foundComments
#                 });
#             } else {
#                 res.json({
#                     status: 400,
#                     data: 'no data found'
#                 });
#             }
#         } else {
#             res.json({
#                 status: 400,
#                 data: 'no user session found'
#             })
#         }
#     }catch(err){
#         console.error(err);
#         next(err);
#     }
# });


users_api = Blueprint('resources.user', __name__)

api = Api(users_api)

api.add_resource(
    UserList,
    '/register/'
)

api.add_resource(
    User,
    '/logout/'
)

api.add_resource(
    GetUserData,
    '/usercomments/'
)

api.add_resource(
    User,
    '/login/',
    endpoint='auth'
)