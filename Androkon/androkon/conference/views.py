from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from conference.models import Conference, Event
from django.core import serializers
from django.http import HttpResponse

#def profile(request):
#	entries = Conference.objects.get(user= )

def json_cons(request):
    json = serializers.serialize("json", Conference.objects.all())
    return HttpResponse(json, mimetype='application/json')

def json_events(request):
    json = serializers.serialize("json", Event.objects.all())
    return HttpResponse(json, mimetype='application/json')
