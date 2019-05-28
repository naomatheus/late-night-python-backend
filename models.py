import datetime

from peewee import *

DATABASE = SqliteDatabase('late-night.sqlite')

# eventually we'll switch to POSTGRES and uncomment this

# DATABASE = PostgresqlDatabase('late-night', user='matton',password='matton')



from flask_bcrypt import generate_password_hash
from flask_login import UserMixin

class User(Model):
	name=CharField()

# DO NOT NEED A COMMENTS MADE OR COMMENT ID HERE

	class Meta:
		database=DATABASE


class Place(Model):
	# name=CharField()

# DO NOT NEED A COMMENT ID or comment key in this table

	class Meta:
		database=DATABASE


class Comment(Model):
	# name=CharField()


	class Meta:
		database=DATABASE

# def initialize():
# 	DATABASE.connect()
# 	DATABASE.create_tabes([name], safe=True)
# 	DATABASE.close()
