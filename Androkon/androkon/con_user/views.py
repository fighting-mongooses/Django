from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from con_user.forms import RegistrationForm, LoginForm
from con_user.models import ConAdmin, SignUpKey
from django.contrib.auth import authenticate, login, logout
from con_user.forms import RegistrationForm
from conference.models import Conference
from random import randint
from datetime import datetime
from django.views.generic import RedirectView

def Invite(request, msg):
	baseUrl = "../../"
	if request.user.is_superuser:
		context = { 'invs' : SignUpKey.objects.all(), 'msg' : msg, 'baseUrl' : baseUrl}
		return render_to_response('invite.html', context, context_instance=RequestContext(request))
	context = {'baseUrl' : baseUrl }
	return render_to_response('denied.html', context, context_instance=RequestContext(request))


def NewInvite(request, key):
	key = int(key)
	baseUrl = "../../../"

	if request.user.is_superuser:
		if key < 111111111 or key > 999999999:
			newKey = randint(111111111, 999999999)

			while SignUpKey.objects.filter(key = newKey).count():
				newKey = randint(111111111, 999999999)
		else:
			newKey = key

   
		invite = SignUpKey(key = newKey, date = datetime.now())
		invite.save()
	
	return HttpResponseRedirect(baseUrl + 'invite')

def DeleteInvite(request, key):
	key = int(key)
	baseUrl = "../../../"
	
	if request.user.is_superuser:
		for k in SignUpKey.objects.all():
			if k.key == key:
				k.delete()
				return HttpResponseRedirect(baseUrl + "invite/" + str(key))

	return HttpResponseRedirect(baseUrl + 'invite')


def ConAdminRegistration(request, key):
	key = int(key)
	
	baseUrl = "../../"
	
	for k in SignUpKey.objects.all():
		if k.key == key:

			if request.user.is_authenticated():
				# If they're already a valid user, send them to their profile page.
				context = {'message' : 'You are already signed in. Send a link to this page to someone to let the sign up.', 'baseUrl' : baseUrl}	
				return render_to_response('denied.html', context, context_instance=RequestContext(request))

			if request.method =='POST':
				# If they're in the process of filling out a form
				form = RegistrationForm(request.POST)
				if form.is_valid():
					user = User.objects.create_user(
						username=form.cleaned_data['username'],
						email=form.cleaned_data['email'],
						password=form.cleaned_data['password'])
					user.save()
					con_user = authenticate(username=form.cleaned_data['username'], password = form.cleaned_data['password'])
					login(request, con_user)
				
					con_user = ConAdmin(user=user, name=form.cleaned_data['name'])
					con_user.save()
					k.delete() # invite used
					return HttpResponseRedirect(baseUrl + 'profile/')
				else:
					context = {'form' : form, 'baseUrl' : baseUrl}
					return render_to_response('register.html', context, context_instance=RequestContext(request))
			else:
				# Show the user a blank registration form
				form = RegistrationForm()
				context = {'form': form, 'baseUrl' : baseUrl}
				return render_to_response('register.html', context, context_instance=RequestContext(request))
	
	context = {'message' : 'You need an invite to sign up to this site. Please contact an administrator.', 'baseUrl' : baseUrl}	
	return render_to_response('denied.html', context, context_instance=RequestContext(request))


def LoginRequest(request):
	baseUrl = "../"

	if request.user.is_authenticated():
		return HttpResponseRedirect(baseUrl + 'profile/')
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			con_user = authenticate(username=username, password = password)
			if con_user is not None:
				login(request, con_user)
				return HttpResponseRedirect(baseUrl + 'profile/')
			else:
				message = "That is an invalid username and password combination. Please try again."
				context = {'form' : form, 'message' : message, 'baseUrl' : baseUrl}
				return render_to_response('login.html', context, context_instance=RequestContext(request))
		else:
			context = {'form' : form, 'baseUrl' : baseUrl }
			return render_to_response('login.html', context, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		context = {'form': form, 'baseUrl' : baseUrl}
		return render_to_response('login.html', context, context_instance=RequestContext(request))

def LogoutRequest(request):
	baseUrl = "../"
	logout(request)
	return HttpResponseRedirect(baseUrl + 'login/')	

# def ProfileRequest(request, username):
# 	user = User.objects.get(username=username)
# 	conuser = request.user.get_profile
# 	message = "Hey, there"
# 	context = {'conuser': conuser, 'user': user, 'username': username, 'message': message}
# 	return render_to_response('profile.html', context, context_instance=RequestContext(request))


def Profile(request):
	baseUrl = "../"

	if not request.user.is_authenticated():
		return HttpResponseRedirect(baseUrl + 'login/')
	con_user = request.user.get_profile
	if request.user.is_superuser:
		cons = Conference.objects.all()
	else:
		cons = Conference.objects.all().filter(user = request.user)
	context = {'con_user': con_user, 'cons': cons, 'baseUrl': baseUrl}
	return render_to_response('profile.html', context, context_instance=RequestContext(request))
