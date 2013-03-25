from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from random import randint

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
	    models.Model.save(self, *args, **kwargs)

def create_conadmin_user_callback(sender, instance, **kwargs):
	con_user, new = ConAdmin.objects.get_or_create(user=instance)

post_save.connect(create_conadmin_user_callback, User)


'''  c = ConAdmin(name="Tom", surname="Gregg", username="tom123", password="asdf", password1="asdf", email="tom1234@gmail.com") '''
'''  c = ConAdmin(name="Tom", surname="Gregg") '''
