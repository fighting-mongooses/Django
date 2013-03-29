from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from random import randint
from conference.models import Conference

class SignUpKey(models.Model):
	key =  models.IntegerField(unique = True, help_text="unique key to allow one signup.")
	date = models.DateTimeField(help_text='Date at which the key was generated.')

	def save(self):
		super(SignUpKey, self).save()

	def __unicode__(self):
		return str(self.key)
	

class ConAdmin(models.Model):
	user 	= models.OneToOneField(User)
	name 	= models.CharField(max_length=100, blank=True)

	def __unicode__(self):
		return self.name


	def save(self, *args, **kwargs):
		try:
			existing = ConAdmin.objects.get(user=self.user)
			self.id = existing.id #force update instead of insert
		except ConAdmin.DoesNotExist:
			pass 
		self.user.save()
		models.Model.save(self, *args, **kwargs)
	
	def delete(self, *args, **kwargs):
		for c in Conference.objects.all().filter(user = self.user):
			c.delete()
		self.user.delete(*args, **kwargs)
		super(ConAdmin, self).delete(*args, **kwargs)



'''  c = ConAdmin(name="Tom", surname="Gregg", username="tom123", password="asdf", password1="asdf", email="tom1234@gmail.com") '''
'''  c = ConAdmin(name="Tom", surname="Gregg") '''
