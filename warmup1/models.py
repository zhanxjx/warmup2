from django.db import models

class User(models.Model):
	name = models.CharField(max_length=128)
	password = models.CharField(max_length=128)
	count = models.IntegerField()
	name.primary_key = True
	
	def __unicode__(self):
		return self.name