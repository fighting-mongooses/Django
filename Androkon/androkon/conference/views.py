from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from conference.models import Conference, Event
from django.core import serializers
from django.http import HttpResponse
from conference.forms import ConferenceForm
from django.views.generic import UpdateView

#def profile(request):
#	entries = Conference.objects.get(user= )

def json_cons(request):
    json = serializers.serialize("json", Conference.objects.all())
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
		data = request.POST.copy()
		data['slug'] = "a" # slugs are handled inside the model, this forces the check to pass
		form = ConferenceForm(data)
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
		context = {'form': form, 'baseUrl' : baseUrl}
		return render_to_response('reg_con.html', context, context_instance=RequestContext(request))

def ConferenceUpdate(UpdateView):
    model = Conference
    form_class = ConferenceForm
    template_name = 'reg_con.html'
    success_url = '/profile/'
