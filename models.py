import datetime

from peewee import *

DATABASE = SqliteDatabase('late-night.sqlite')

# eventually we'll switch to POSTGRES and uncomment this

# DATABASE = PostgresqlDatabase('late-night', user='matton',password='matton')



from flask_bcrypt import generate_password_hash
from flask_login import UserMixin

class User(Model):
	username=CharField()
	password=CharField()
	email=CharField()
	# not sure if email/pw need to be required

# DO NOT NEED A COMMENTS MADE OR COMMENT ID HERE

	class Meta:
		database=DATABASE


class Restaurant(Model):
	name=CharField()
	address=CharField()
	place_id=CharField()

# DO NOT NEED A COMMENT ID or comment key in this table

	class Meta:
		database=DATABASE


class Comment(Model):
	comment_author=ForeignKeyField(User)
	comment_body=CharField()
	place_id=ForeignKeyField(Restaurant)




	class Meta:
		database=DATABASE

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User], safe=True)
	DATABASE.close()
