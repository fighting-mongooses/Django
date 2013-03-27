from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Conference(models.Model):

	# Core fields:
	name 		= models.CharField(max_length=100, help_text='The name of the conference. Maximum 100 characters.')
	description = models.TextField(help_text='A description of the conference.')
	start_date 	= models.DateTimeField(help_text='Start date and time for the conference.')
	end_date 	= models.DateTimeField(help_text='End date and time for the conference.')
	twitter 	= models.CharField(max_length=50, help_text='The twitter account of the conference')
	website     = models.URLField(help_text='The website of the conference')
	guests		= models.TextField(help_text='A description of any guest speakers attending the conference', blank=True)
	enabled     = models.BooleanField(help_text='Whether or not this conference is to be displayed to users', default=True)
	# Meta data:
	user = models.ForeignKey(User)

	def __unicode__(self):
		return self.name

	def save(self):
		#baseSlug = slugify(self.name)
		#newSlug = baseSlug
		#num = 1
		#while Conference.objects.filter(slug = newSlug).count():
		#	newSlug = baseSlug + str(num)
		#	num += 1
		#
		#self.slug = newSlug
		super(Conference, self).save()

	def get_absolute_url(self):
		return "%s/" % self.slug


class Event(models.Model):

	name 		= models.CharField(max_length="50", help_text="The name of the event. Maximum 50 characters.")
	description = models.TextField(help_text="A description of the event.")
	time 		= models.DateTimeField(help_text="Time and date for the event")
	conference 	= models.ForeignKey(Conference)
	enabled     = models.BooleanField(help_text='Whether or not this event is to be displayed to users', default=True)


	def __unicode__(self):
		return self.name

	def save(self):
		super(Event, self).save()

	def get_absolute_url(self):
		return "%s/" % self.slug
