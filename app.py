from flask import Flask, g, jsonify
from flask_login import LoginManager
import models
from flask_cors import CORS
from resources.users import users_api
from resources.restaurants import restaurants_api
from resources.comments import comments_api
from flask_login import current_user

import config

login_manager = LoginManager()

DEBUG = True
PORT = 8000

app = Flask(__name__)

app.secret_key = config.SECRET_KEY

login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
	try:
		return models.User.get(models.User.id==userid)
	except models.DoesNotExist:
		return None

CORS(users_api, origin=['http://localhost:3000','http://localhost:8000'], supports_credentials=True, allow_headers='*')
CORS(restaurants_api, origin=['http://localhost:3000','http://localhost:8000'], supports_credentials=True, allow_headers='*')
CORS(comments_api, origin=['http://localhost:3000', 'http://localhost:8000'], supports_credentials=True, allow_headers='*')

app.register_blueprint(users_api, url_prefix='/auth')
app.register_blueprint(restaurants_api, url_prefix='/restaurants')
app.register_blueprint(comments_api, url_prefix='/comment')

@app.before_request
def before_request():
	"""Connect to the DB before each request"""
	g.db = models.DATABASE
	g.db.connect()
	g.user = current_user
	g.user._get_current_object()

@app.after_request
def after_request(response):
	"""Close connection to DB after each rq"""
	g.db.close()
	return response

# @app.route('/test')
# def get_data():
# 	return requests.get(config.API_URL + API_KEY).content


@app.route('/')
def index():
	return 'Welcome to Late Night Bytes'

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG,port=PORT)