from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class ConAdmin(models.Model):
	user 	= models.OneToOneField(User)
	name 	= models.CharField(max_length=15)
	surname = models.CharField(max_length=15)
	
	def __unicode__(self):
		return self.name

def create_conadmin_user_callback(sender, instance, **kwargs):
	con_user, new = ConAdmin.objects.get_or_create(user=instance)

post_save.connect(create_conadmin_user_callback, User)


'''  c = ConAdmin(name="Tom", surname="Gregg", username="tom123", password="asdf", password1="asdf", email="tom1234@gmail.com") '''
''' c = ConAdmin(name="Tom", surname="Gregg") '''