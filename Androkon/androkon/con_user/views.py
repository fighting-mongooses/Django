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

def Invite(request, msg):
	if request.user.is_superuser:
		context = { 'invs' : SignUpKey.objects.all(), 'msg' : msg }
		return render_to_response('invite.html', context, context_instance=RequestContext(request))
	return render_to_response('denied.html')


def NewInvite(request, key):
	key = int(key)

	if request.user.is_superuser:
		if key == -1:
			newKey = randint(0, 999999999)

			while SignUpKey.objects.filter(key = newKey).count():
				newKey = randint(0, 999999999)
		else:
			newKey = key

   
		invite = SignUpKey(key = newKey, date = datetime.now())
		invite.save()

	return redirect('con_user.views.Invite')

def DeleteInvite(request, key):
	key = int(key)

	for k in SignUpKey.objects.all():
		if k.key == key:
			k.delete()
			return Invite(request, str(key))

	return redirect('con_user.views.Invite')


def ConAdminRegistration(request, key):
	key = int(key)
	
	for k in SignUpKey.objects.all():
		if k.key == key:

			if request.user.is_authenticated():
				# If they're already a valid user, send them to their profile page.
				return HttpResponseRedirect('/profile/')
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
					return redirect('con_user.views.Profile')
				else:
					return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))
			else:
				# Show the user a blank registration form
				form = RegistrationForm()
				context = {'form': form}
				return render_to_response('register.html', context, context_instance=RequestContext(request))
	
	context = {'message' : 'You need an invite to sign up to this site. Please contact an administrator.'}	
	return render_to_response('denied.html', context, context_instance=RequestContext(request))


def LoginRequest(request):

	if request.user.is_authenticated():
		return HttpResponseRedirect('/profile/')
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			con_user = authenticate(username=username, password = password)
			if con_user is not None:
				login(request, con_user)
				return HttpResponseRedirect('/profile/')
			else:
				message = "That is an invalid username and password combination. Please try again."
				return render_to_response('login.html', {'form': form, 'message': message}, context_instance=RequestContext(request))
		else:
			return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
	else:
		form = LoginForm()
		context = {'form': form}
		return render_to_response('login.html', context, context_instance=RequestContext(request))

def LogoutRequest(request):
	logout(request)
	return HttpResponseRedirect('/login/')	

def ProfileRequest(request, username):
	user = User.objects.get(username=username)
	conuser = request.user.get_profile
	message = "Hey, there"
	context = {'conuser': conuser, 'user': user, 'username': username, 'message': message}
	return render_to_response('profile.html', context, context_instance=RequestContext(request))


def Profile(request):
    if not request.user.is_authenticated():
		return redirect('con_user.views.LoginRequest')
    con_user = request.user.get_profile
    message = "Bottom"
    name = request.user.username
    cons = Conference.objects.all().filter(user = request.user)
    context = {'con_user': con_user, 'message': message, 'name': name, 'cons': cons}
    return render_to_response('profile.html', context, context_instance=RequestContext(request))
