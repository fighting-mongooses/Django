from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from random import randint
from conference.models import Conference


#Class to represent a key required for registration
class SignUpKey(models.Model):
	key =  models.IntegerField(unique = True, help_text="unique key to allow one signup.")
	date = models.DateTimeField(help_text='Date at which the key was generated.')

	def save(self):
		super(SignUpKey, self).save()

	def __unicode__(self):
		return str(self.key)
	
#Class to represent a user who interacts with the website
class ConAdmin(models.Model):
	user 	= models.OneToOneField(User)
	name 	= models.CharField(max_length=100, blank=True)

	def __unicode__(self):
		return self.name

	#Over-ride the save() method
	def save(self, *args, **kwargs):
		try:
			existing = ConAdmin.objects.get(user=self.user)
			self.id = existing.id #force update instead of insert
		except ConAdmin.DoesNotExist:
			pass 
		self.user.save()
		models.Model.save(self, *args, **kwargs)

	#Over-ride the delete() method
	def delete(self, *args, **kwargs):
		for c in Conference.objects.all().filter(user = self.user):
			c.delete()
		self.user.delete(*args, **kwargs)
		super(ConAdmin, self).delete(*args, **kwargs)