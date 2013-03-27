from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from conference.models import Conference, Event
from django.core import serializers
from django.http import HttpResponse
from conference.forms import ConferenceForm
from django.views.generic import UpdateView
from django.template.defaultfilters import slugify

#def profile(request):
#	entries = Conference.objects.get(user= )

def json_cons(request):
	json = serializers.serialize("json", Conference.objects.filter(enabled = True))
	return HttpResponse(json, mimetype='application/json')

def json_events(request):
	json = serializers.serialize("json", Event.objects.all())
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
				user=request.user)
			conference.save()
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
				con.save()
				return HttpResponseRedirect(baseUrl + 'profile/')

			else:
				context = { 'form' : form, 'baseUrl' : baseUrl }
				return render_to_response('reg_con.html', context, context_instance=RequestContext(request))

		else:
			form = ConferenceForm({
				'name': con.name, 'description': con.description, 'start_date': con.start_date,
				'end_date': con.end_date, 'twitter': con.twitter, 'website': con.website, 'guests': con.guests})

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
		context = {'baseUrl': baseUrl, 'message': 'You do not have permission to delete this conference.'}
		return render_to_response('denied.html', context, context_instance=RequestContext(request))

