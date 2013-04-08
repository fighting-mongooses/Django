from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from conference.models import *
from django.core.exceptions import ValidationError

class ConferenceForm(ModelForm):

	name 		= forms.CharField(label=(u'Name of the Conference'))
	description = forms.CharField(label=(u'Description of the Conference'), widget=forms.Textarea(), required=False)
	start_date	= forms.DateField(("%d/%m/%Y",), label=(u'Start Date of the Conference'), widget=forms.DateTimeInput(attrs={'style' : 'height : 30px'},
			 format="%d/%m/%Y"))
	end_date	= forms.DateField(("%d/%m/%Y",), label=(u'End Date of the Conference'), widget=forms.DateTimeInput(attrs={'style' : 'height : 30px'},
			 format="%d/%m/%Y"), required=False)
	twitter		= forms.CharField(label=(u'Username of the Twitter account associated with the event'), required=False)
	website		= forms.URLField(label=(u'Website for the Conference'), required=False)
	guests		= forms.CharField(label=(u'Description of guest speakers or special guests attending the event'), widget=forms.Textarea(), required=False)
	gmaps 		= forms.CharField(label=(u'Google maps link'), required=False)

	#pictures 	= forms.ImageField(widget=forms.FileInput())

	class Meta:
		model = Conference
		exclude = ('user', 'enabled')

class EventForm(ModelForm):

	
	name 		= forms.CharField(label=(u'Name of the Event'))
	description = forms.CharField(label=(u'Description of the Event'), widget=forms.Textarea(), required=False)
	time	= forms.DateTimeField(("%d/%m/%Y %H:%M",), label=(u'Start Date of the Event'), 
		widget=forms.DateTimeInput(attrs={'style' : 'height : 30px'}, format="%d/%m/%Y %H:%M"))
	end_time	= forms.DateTimeField(("%d/%m/%Y %H:%M",), label=(u'Start Date of the Event'),
		 widget=forms.DateTimeInput(attrs={'style' : 'height : 30px'}, format="%d/%m/%Y %H:%M"), required=False)
	location 		= forms.CharField(label=(u'Location of the event:'), widget=forms.Textarea(), required=False)
	class Meta:
		model = Event
		exclude = ('conference', 'enabled')


class MapForm(ModelForm):
	
	picture = forms.ImageField(widget=forms.FileInput())
	
	def clean_picture(self):
		allowed_size = 1
		image = self.cleaned_data.get('picture',False)
		if image:
			if image._size > allowed_size*1024*1024:
				raise ValidationError("Image file too large ( > " + str(allowed_size) + "mb )")
			return image
		else:
			raise ValidationError("Couldn't read uploaded image")
	
	class Meta:
		model = Map
		exclude = ('conference')
