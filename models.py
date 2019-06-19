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
	id=PrimaryKeyField(null=False)
	user_id=ForeignKeyField(User, related_name='user')
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
	id=PrimaryKeyField(null=False)
	comment_author_id=ForeignKeyField(User, related_name='user')
	commentBody=CharField()
	restaurant_id=ForeignKeyField(Restaurant, related_name='restaurant')


	class Meta:
		database=DATABASE

	@classmethod
	def create_comment(cls, commentAuthor, commentBody, **kwargs):
		try:
			cls.select().where(
				(cls.user_id==user_id)
			).get()
		except cls.DoesNotExist:
			comment = cls(commentAuthor=commentAuthor, commentBody=commentBody)
			comment.save()
			return comment
		else:
			raise Exception('could not find comment')

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Restaurant, Comment], safe=True)
	DATABASE.close()