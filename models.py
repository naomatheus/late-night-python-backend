import datetime

import config

from peewee import *

DATABASE = PostgresqlDatabase('late_night_python', user='clayton', password=config.SQL_PASSWORD)


from flask_bcrypt import generate_password_hash
from flask_login import UserMixin

class User(UserMixin, Model):
	id=PrimaryKeyField(null=False)
	userName=CharField()
	password=CharField()
	email=CharField()
	# not sure if email/pw need to be required

# DO NOT NEED A COMMENTS MADE OR COMMENT ID HERE

	class Meta:
		database=DATABASE

	@classmethod
	def create_users(cls, userName, email, password, **kwargs):
		email = email.lower()
		try:
			cls.select().where(
				(cls.email==email)
			).get()
		except cls.DoesNotExist:
			users = cls(userName=userName, email=email)
			users.password = generate_password_hash(password)
			users.save()
			return users
		else:
			raise Exception('user with that email already exists')

class Restaurant(Model):
	user_id=ForeignKeyField(User, related_name='user')
	id=PrimaryKeyField(null=False)
	name=CharField()
	address=CharField()
	place_id=CharField()

# DO NOT NEED A COMMENT ID or comment key in this table

	class Meta:
		database=DATABASE

	@classmethod
	def create_restaurant(cls, user_id, name, address, place_id, **kwargs):
		try:
			cls.select().where(
				(cls.place_id==place_id)
			).get()
		except cls.DoesNotExist:
			restaurant = cls(name=name, address=address)
			restaurant.save()
			return restaurant
		else:
			raise Exception('could not find restaurant')


class Comment(Model):
	user_id=ForeignKeyField(User, related_name='user')
	id=PrimaryKeyField(null=False)
	comment_author=ForeignKeyField(User)
	comment_body=CharField()
	place_id=ForeignKeyField(Restaurant)


	class Meta:
		database=DATABASE

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Restaurant, Comment], safe=True)
	DATABASE.close()