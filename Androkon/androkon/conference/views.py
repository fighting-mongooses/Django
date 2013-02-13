from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from conference.models import Conference

def profile(request):
	entries = Conference.objects.get(user= )