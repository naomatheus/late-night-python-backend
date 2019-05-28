import datetime

from peewee import *

DATABASE = 

class Name(Model):
	name=CharField()




	class Meta:
		database=DATABASE


# def initialize():
# 	DATABASE.connect()
# 	DATABASE.create_tabes([name], safe=True)
# 	DATABASE.close()
