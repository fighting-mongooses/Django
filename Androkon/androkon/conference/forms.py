from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from conference.models import Conference

class ConferenceForm(ModelForm):

	name 		= forms.CharField(label=(u'Name of the Conference'))
	description = forms.CharField(label=(u'Description of the Conference'), widget=forms.Textarea())
	start_date	= forms.DateTimeField(label=(u'Start Date of the Conference'), widget=forms.DateInput())
	end_date	= forms.DateTimeField(label=(u'End Date of the Conference'), widget=forms.DateInput())
	twitter		= forms.CharField(label=(u'Username of the Twitter account associated with the event'))
	website		= forms.URLField(label=(u'Website for the Conference'))
	guests		= forms.CharField(label=(u'Description of guest speakers or special guests attending the event'), widget=forms.Textarea(), required=False)

	class Meta:
		model = Conference
		exclude = ('user',)