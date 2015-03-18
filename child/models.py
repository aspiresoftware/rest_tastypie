from django.db import models
from django.core.urlresolvers import reverse

class Child(models.Model):
	first_name = models.CharField(max_length=45)
	last_name = models.CharField(max_length=45)
	email = models.EmailField()
	mobile = models.IntegerField()

	def __unicode__(self):
		return self.first_name

	def get_absolute_url(self):
		return reverse('child_edit', kwargs={'pk': self.pk})