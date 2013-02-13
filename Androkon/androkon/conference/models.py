from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Conference(models.Model):

	# Core fields:
	name 		= models.CharField(max_length=100, help_text='The name of the conference. Maximum 100 characters.')
	slug 		= models.SlugField(unique=True)
	description = models.TextField(help_text='A description of the conference.')
	start_date 	= models.DateTimeField(help_text='Start date and time for the conference.')
	end_date 	= models.DateTimeField(help_text='End date and time for the conference.')

	# Meta data:
	user = models.ForeignKey(User)

	def __unicode__(self):
		return self.name

	def save(self):
		self.slugs = slugify(self.name)
		super(Conference, self).save()

	def get_absolute_url(self):
		return "%s/" % self.slug


class Event(models.Model):

	name 		= models.CharField(max_length="50", help_text="The name of the event. Maximum 50 characters.")
	slug 		= models.SlugField(unique=True)
	description = models.TextField(help_text="A description of the event.")
	time 		= models.DateTimeField(help_text="time and date for the event")
	conference 	= models.ForeignKey(Conference)

	def __unicode__(self):
		return self.name

	def save(self):
		self.slug = slugify(self.name)
		super(Event, self).save()

	def get_absolute_url(self):
		return "%s/" % self.slug