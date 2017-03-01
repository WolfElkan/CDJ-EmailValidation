from __future__ import unicode_literals
from django.db import models, connection
from datetime import datetime
import re

# Create your models here.

class Validation(object):
	def __init__(self, field, regex, error):
		self.field = field
		self.regex = regex
		self.error = error
	def __valid(self, datum):
		return re.match(self.regex, datum) != None
	def isValid(self, datum, andLast=True):
		return andLast and self.__valid(datum)
	def errors(self, datum, messages):
		if not self.__valid(datum):
			messages += [self.error]
		return messages

class Confirmation(Validation):
	def __valid(self, datum):
		return datum == self.regex


class EmailManager(models.Manager):
	validations = [
		Validation('email',r'^[\w.+-]+@[\w.+-]+\.[a-zA-Z]+$',"Email is not valid!"),
		Validation('email',r'^.{,45}$',"Email is too long"),
	]
	def isValid(self, data):
		valid = True
		for x in self.validations:
			datum = data[x.field]
			valid = x.isValid(datum, valid)
		return valid
	def errors(self, data):
		messages = []
		for x in self.validations:
			datum = data[x.field]
			messages = x.errors(datum, messages)
		return messages
	def create(self, data):
		if self.isValid(data):
			sql = "INSERT INTO main_Email (email, created_at, updated_at) VALUES ('{}', '{}', '{}')"
			sql = sql.format(data['email'],datetime.now(),datetime.now())
			print "SQL:", sql
			with connection.cursor() as cursor:
				cursor.execute(sql)


class Email(models.Model):
	email = models.CharField(max_length=45)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = EmailManager()





