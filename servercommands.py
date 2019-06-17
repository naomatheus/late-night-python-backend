# virtualenv .env -p python3

# source .env/bin/activate

# pip3 install flask-restful peewee flask psycopg2 flask_login flask_cors

# GetUserComents class
# class GetUserComments(Resource):
# 	def __init__(self):
# 		self.reqparse = reqparse.RequestParser()
# 		self.reqparse.add_argument(
# 			'commentAuthor',
# 			required=True,
# 			help='no comment author provided',
# 			location='form'
# 		)
# 		self.reqparse.add_argument(
# 			'commentBody',
# 			required=True,
# 			help='no comment body provided',
# 			location='json'
# 		)
# 		self.reqparse.add_argument(
# 			'restaurant_name',
# 			required=True,
# 			help='no restaurant name provided',
# 			location='json'
# 		)
# 		self.reqparse.add_argument(
# 			'restaurant_id',
# 			required=True,
# 			help='no restaurant id provided',
# 			location='json'
# 		)
# 		super().__init__()