from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from conference.models import Conference, Event
from django.core import serializers
from django.http import HttpResponse
from conference.forms import *
from django.views.generic import UpdateView
from django.template.defaultfilters import slugify

#def profile(request):
#	entries = Conference.objects.get(user= )

def json_cons(request):
	json = serializers.serialize("json", Conference.objects.filter(enabled = True))
	return HttpResponse(json, mimetype='application/json')

def json_events(request):
	events = []
	for e in Event.objects.all():
		if e.enabled and e.conference.enabled:
			events.append(e)

	json = serializers.serialize("json", events)
	return HttpResponse(json, mimetype='application/json')


def ConferenceRegistration(request):
	baseUrl = "../"	

	if not request.user.is_authenticated():
		return HttpResponseRedirect(baseUrl + 'login/')
	if request.method =='POST':
		# If they're in the process of filling out a form
		#data = request.POST.copy()
		#data['slug'] = "a" # slugs are handled inside the model, this forces the check to pass
		form = ConferenceForm(request.POST)
		if form.is_valid():
			conference = Conference(
				name=form.cleaned_data['name'],
				description=form.cleaned_data['description'],
				start_date=form.cleaned_data['start_date'],
				end_date=form.cleaned_data['end_date'],
				twitter=form.cleaned_data['twitter'],
				website=form.cleaned_data['website'],
				guests=form.cleaned_data['guests'],
				gmaps=form.cleaned_data['gmaps'],
				user=request.user)
			conference.save()
			#pic = PhotoUpload(con = conference, picture=form.cleaned_data['pictures'])
			return HttpResponseRedirect(baseUrl + 'profile/')
		else:
			context = { 'form' : form, 'baseUrl' : baseUrl }
			return render_to_response('reg_con.html', context, context_instance=RequestContext(request))
	else:
		# Show the user a blank registration form
		form = ConferenceForm()
		context = {'form': form, 'baseUrl': baseUrl}
		return render_to_response('reg_con.html', context, context_instance=RequestContext(request))

def ConferenceUpdate(request, key):
	baseUrl = "../../"
	
	try:
		con = Conference.objects.get(pk=key)
	except Conference.DoesNotExist:
		context = {'baseUrl': baseUrl, 'message': 'Invalid con id.'}
		return render_to_response('denied.html', context, context_instance=RequestContext(request))
	
	if request.user == con.user or request.user.is_superuser:
		if request.method =='POST':
			form = ConferenceForm(request.POST)
			if form.is_valid():
				con.name = form.cleaned_data['name']
				con.description = form.cleaned_data['description']
				con.start_date = form.cleaned_data['start_date']
				con.end_date = form.cleaned_data['end_date']
				con.twitter = form.cleaned_data['twitter']
				con.website = form.cleaned_data['website']
				con.guests = form.cleaned_data['guests']
				con.gmaps = form.cleaned_data['gmaps']
				con.save()
				return HttpResponseRedirect(baseUrl + 'profile/')

			else:
				context = { 'form' : form, 'baseUrl' : baseUrl }
				return render_to_response('reg_con.html', context, context_instance=RequestContext(request))

		else:
			form = ConferenceForm({
				'name': con.name, 'description': con.description, 'start_date': con.start_date,
				'end_date': con.end_date, 'twitter': con.twitter, 'website': con.website, 'guests': con.guests, 'gmaps': con.gmaps})

			context = { 'form' : form, 'baseUrl' : baseUrl }
			return render_to_response('reg_con.html', context, context_instance=RequestContext(request))
	 
 
	else:
		context = {'baseUrl': baseUrl, 'message': 'You do not have permission to edit this conference.'}
		return render_to_response('denied.html', context, context_instance=RequestContext(request))

   
def DeleteCon(request, key):
	baseUrl = "../../"
	
	try:
		con = Conference.objects.get(pk=key)
	except Conference.DoesNotExist:
		context = {'baseUrl': baseUrl, 'message': 'Invalid con id.'}
		return render_to_response('denied.html', context, context_instance=RequestContext(request))
		
	if request.user == con.user or request.user.is_superuser:
		con.enabled = False
		con.save()
		return HttpResponseRedirect(baseUrl + "profile/")
	else:
		context = {'baseUrl': baseUrl, 'message': 'You do not have permission to delete this conference.'}
		return render_to_response('denied.html', context, context_instance=RequestContext(request))

def NukeCon(request, key):
	baseUrl = "../../"
	
	try:
		con = Conference.objects.get(pk=key)
	except Conference.DoesNotExist:
		context = {'baseUrl': baseUrl, 'message': 'Invalid con id.'}
		return render_to_response('denied.html', context, context_instance=RequestContext(request))
		
	if request.user == con.user or request.user.is_superuser:
		for e in Event.objects.all().filter(conference = con):
			e.delete()
		con.delete()	
		return HttpResponseRedirect(baseUrl + "profile/")
	else:
		context = {'baseUrl': baseUrl, 'message': 'You do not have permission to delete this conference.'}
		return render_to_response('denied.html', context, context_instance=RequestContext(request))



def RestoreCon(request, key):
	baseUrl = "../../"
	
	try:
		con = Conference.objects.get(pk=key)
	except Conference.DoesNotExist:
		context = {'baseUrl': baseUrl, 'message': 'Invalid con id.'}
		return render_to_response('denied.html', context, context_instance=RequestContext(request))
		
	if request.user == con.user or request.user.is_superuser:
		con.enabled = True
		con.save()
		return HttpResponseRedirect(baseUrl + "profile/")
	else:
		context = {'baseUrl': baseUrl, 'message': 'You do not have permission to modify this conference.'}
		return render_to_response('denied.html', context, context_instance=RequestContext(request))


def ManageEvents(request, key):
	baseUrl = "../../"

	try:
		con = Conference.objects.get(pk=key)
	except Conference.DoesNotExist:
		context = {'baseUrl': baseUrl, 'message': 'Invalid con id.'}
		return render_to_response('denied.html', context, context_instance=RequestContext(request))
		
	if request.user == con.user or request.user.is_superuser:
		context = {'baseUrl': baseUrl, 'events': Event.objects.filter(conference = con), 'con': con}
		return render_to_response('manage_events.html', context, context_instance=RequestContext(request))

	else:
		context = {'baseUrl': baseUrl, 'message': 'You do not have permission to modify this conference.'}
		return render_to_response('denied.html', context, context_instance=RequestContext(request))


def AddEvent(request, key):
	baseUrl = "../../"

	try:
		con = Conference.objects.get(pk=key)
	except Conference.DoesNotExist:
		context = {'baseUrl': baseUrl, 'message': 'Invalid con id.'}
		return render_to_response('denied.html', context, context_instance=RequestContext(request))
		
	if request.user == con.user or request.user.is_superuser:

		if request.method =='POST':
			form = EventForm(request.POST)
			if form.is_valid():
				event = Event(
					name = form.cleaned_data['name'],
					description = form.cleaned_data['description'],
					time = form.cleaned_data['time'],
					end_time = form.cleaned_data['end_time'],
					location = form.cleaned_data['location'],
					conference = con,
					)

				event.save()
				return HttpResponseRedirect(baseUrl+'manage_events/'+str(event.conference.id)+"/")
			else:
				context = {'baseUrl': baseUrl, 'form': form}
				return render_to_response('create_event.html', context, context_instance=RequestContext(request))

		else:
			form = EventForm()
			context = {'baseUrl': baseUrl, 'form': form}
			return render_to_response('create_event.html', context, context_instance=RequestContext(request))

	else:
		context = {'baseUrl': baseUrl, 'message': 'You do not have permission to dmodify this conference'}
		return render_to_response('denied.html', context, context_instance=RequestContext(request))


def EditEvent(request, key):
	baseUrl = "../../"

	try:
		event = Event.objects.get(pk=key)
	except Event.DoesNotExist:
		context = {'baseUrl': baseUrl, 'message': 'Invalid event id.'}
		return render_to_response('denied.html', context, context_instance=RequestContext(request))
		
	if request.user == event.conference.user or request.user.is_superuser:

		if request.method =='POST':
			form = EventForm(request.POST)
			if form.is_valid():
				event.name = form.cleaned_data['name']
				event.description = form.cleaned_data['description']
				event.time = form.cleaned_data['time']

				event.save()
				return HttpResponseRedirect(baseUrl+'manage_events/'+str(event.conference.id)+"/")
			else:
				context = {'baseUrl': baseUrl, 'form': form}
				return render_to_response('create_event.html', context, context_instance=RequestContext(request))

		else:
			form = EventForm({'name': event.name, 'description': event.description, 'time': event.time, 'end_time': event.end_time, 'location': event.location})
			context = {'baseUrl': baseUrl, 'form': form}
			return render_to_response('create_event.html', context, context_instance=RequestContext(request))

	else:
		context = {'baseUrl': baseUrl, 'message': 'You do not have permission to modify this event.'}
		return render_to_response('denied.html', context, context_instance=RequestContext(request))

   
def DeleteEvent(request, key):
	baseUrl = "../../"
	
	try:
		event = Event.objects.get(pk=key)
	except Event.DoesNotExist:
		context = {'baseUrl': baseUrl, 'message': 'Invalid event id.'}
		return render_to_response('denied.html', context, context_instance=RequestContext(request))
		
	if request.user == event.conference.user or request.user.is_superuser:
		event.enabled = False
		event.save()
		return HttpResponseRedirect(baseUrl + "manage_events/" + str(event.conference.id))  
	else:
		context = {'baseUrl': baseUrl, 'message': 'You do not have permission to delete this event.'}
		return render_to_response('denied.html', context, context_instance=RequestContext(request))

def NukeEvent(request, key):
	baseUrl = "../../"
	
	try:
		event = Event.objects.get(pk=key)
	except Event.DoesNotExist:
		context = {'baseUrl': baseUrl, 'message': 'Invalid event id.'}
		return render_to_response('denied.html', context, context_instance=RequestContext(request))
		
	if request.user == event.conference.user or request.user.is_superuser:
		event.delete()
		return HttpResponseRedirect(baseUrl + "manage_events/" + str(event.conference.id))  
	else:
		context = {'baseUrl': baseUrl, 'message': 'You do not have permission to delete this event.'}
		return render_to_response('denied.html', context, context_instance=RequestContext(request))




def RestoreEvent(request, key):
	baseUrl = "../../"
	
	try:
		event = Event.objects.get(pk=key)
	except Event.DoesNotExist:
		context = {'baseUrl': baseUrl, 'message': 'Invalid event id.'}
		return render_to_response('denied.html', context, context_instance=RequestContext(request))
		
	if request.user == event.conference.user or request.user.is_superuser:
		event.enabled = True
		event.save()
		return HttpResponseRedirect(baseUrl + "manage_events/" + str(event.conference.id))  
	else:
		context = {'baseUrl': baseUrl, 'message': 'You do not have permission to modify this event.'}
		return render_to_response('denied.html', context, context_instance=RequestContext(request))



