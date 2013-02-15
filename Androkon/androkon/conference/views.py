from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from conference.models import Conference, Event
from django.core import serializers
from django.http import HttpResponse

#def profile(request):
#	entries = Conference.objects.get(user= )

def JSON(request):
    json = serializers.serialize("json", Conference.objects.all())
    json += serializers.serialize("json", Event.objects.all())
    
    return HttpResponse(json, mimetype='application/json')
