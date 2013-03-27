from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from conference.models import *

class ConferenceForm(ModelForm):

	name 		= forms.CharField(label=(u'Name of the Conference'))
	description = forms.CharField(label=(u'Description of the Conference'), widget=forms.Textarea())
	start_date	= forms.DateTimeField(("%d/%m/%Y %H:%M:%S",), label=(u'Start Date of the Conference'), widget=forms.DateTimeInput(attrs={'style' : 'height : 30px'}, format="%d/%m/%Y %H:%M:%S"))
	end_date	= forms.DateTimeField(("%d/%m/%Y %H:%M:%S",), label=(u'End Date of the Conference'), widget=forms.DateTimeInput(attrs={'style' : 'height : 30px'}, format="%d/%m/%Y %H:%M:%S"))
	twitter		= forms.CharField(label=(u'Username of the Twitter account associated with the event'))
	website		= forms.URLField(label=(u'Website for the Conference'))
	guests		= forms.CharField(label=(u'Description of guest speakers or special guests attending the event'), widget=forms.Textarea(), required=False)

	#pictures 	= forms.ImageField(widget=forms.FileInput())

	class Meta:
		model = Conference
		exclude = ('user', 'enabled')

class EventForm(ModelForm):

	
	name 		= forms.CharField(label=(u'Name of the Event'))
	description = forms.CharField(label=(u'Description of the Event'), widget=forms.Textarea())
	time	= forms.DateTimeField(("%d/%m/%Y %H:%M:%S",), label=(u'Start Date of the Event'), widget=forms.DateTimeInput(attrs={'style' : 'height : 30px'}, format="%d/%m/%Y %H:%M:%S"))
	class Meta:
		model = Event
		exclude = ('conference', 'enabled')
