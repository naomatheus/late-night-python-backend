import datetime

from peewee import *

DATABASE = SqliteDatabase('late-night.sqlite')

# eventually we'll switch to POSTGRES and uncomment this

# DATABASE = PostgresqlDatabase('late-night', user='matton',password='matton')



from flask_bcrypt import generate_password_hash
from flask_login import UserMixin

class User(UserMixin, Model):
	username=CharField()
	password=CharField()
	email=CharField()
	# not sure if email/pw need to be required

# DO NOT NEED A COMMENTS MADE OR COMMENT ID HERE

	class Meta:
		database=DATABASE

	@classmethod
	def create_user(cls, username, email, password, **kwargs):
		email = email.lower()
		try:
			cls.select().where(
				(cls.email==email)
			).get()
		except cls.DoesNotExist:
			user = cls(username=username, email=email)

			user.password = generate_password_hash(password)
			user.save()
			return user
		else:
			raise Exception('user with that email already exists')



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
