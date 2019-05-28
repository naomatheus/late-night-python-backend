from flask import Flask, g, jsonify
from flask_login import LoginManager
import models
from flask_cors import CORS
from resources.users import users_api

import config

login_manager = LoginManager()

DEBUG = True
PORT = 8000

app = Flask(__name__)

CORS(users_api, origin=['http://localhost:8000'], supports_credentials=True)

app.register_blueprint(users_api, url_prefix='/users')

@app.before_request
def before_request():
	"""Connect to the DB before each request"""
	g.db = models.DATABASE
	g.db.connect()

@app.after_request
def after_request(response):
	"""Close connection to DB after each rq"""
	g.db.close()
	return response


@app.route('/')
def index():
	return 'hi'

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG,port=PORT)
