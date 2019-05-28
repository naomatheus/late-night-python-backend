from flask import Flask, g
import models

DEBUG = True
PORT = 8000

app = Flask(__name__)

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
