from django.contrib.auth.models import User
from django.db import models
import datetime
from django.core.urlresolvers import reverse

class Child(models.Model):
	user = models.ForeignKey(User)
	first_name = models.CharField(max_length=45)
	last_name = models.CharField(max_length=45)
	email = models.EmailField()
	mobile = models.IntegerField()

	def __unicode__(self):
		return self.first_name

class UserLogin(models.Model):
	user = models.ForeignKey(User)
	access_token = models.CharField(max_length=100)
	refresh_token = models.CharField(max_length=100)
	expire_date = models.DateTimeField()
