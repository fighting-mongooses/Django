from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from con_user.forms import *
from con_user.models import *
from django.contrib.auth import authenticate, login, logout
from con_user.forms import RegistrationForm
from conference.models import Conference
from random import randint
from datetime import datetime
from django.views.generic import RedirectView


# Method for returning all unused invite keys
def Invite(request, msg):
	baseUrl = "../../"
	if request.user.is_superuser:
		context = { 'invs' : SignUpKey.objects.all(), 'msg' : msg, 'baseUrl' : baseUrl}
		return render_to_response('invite.html', context, context_instance=RequestContext(request))
	context = {'baseUrl' : baseUrl }
	return render_to_response('denied.html', context, context_instance=RequestContext(request))

# Method for generating a new invite key
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

# Method for deleting an invite key
def DeleteInvite(request, key):
	key = int(key)
	baseUrl = "../../../"
	
	if request.user.is_superuser:
		for k in SignUpKey.objects.all():
			if k.key == key:
				k.delete()
				return HttpResponseRedirect(baseUrl + "invite/" + str(key))

	return HttpResponseRedirect(baseUrl + 'invite')

# Method for registering a user
def ConAdminRegistration(request, key):
	key = int(key)
	
	baseUrl = "../../"
	# Validate the key
	for k in SignUpKey.objects.all():
		if k.key == key:

			if request.user.is_authenticated():
				# If they're already a valid user, send them to their profile page.
				context = {'message' : 'You are already signed in. Send a link to this page to someone to let them sign up.', 'baseUrl' : baseUrl}	
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

# Method for loggin-in a user
def LoginRequest(request):
	baseUrl = "../"

	if request.user.is_authenticated():
		# If they're already a valid user, send them to their profile page.
		return HttpResponseRedirect(baseUrl + 'profile/')
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			con_user = authenticate(username=username, password = password)
			if con_user is not None:
				if not con_user.is_active:
					context = {'baseUrl': baseUrl, 'message': 'You are banned'}
					return render_to_response('denied.html', context, context_instance=RequestContext(request))

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

# Method for changing a users password
def PassWordChange(request, key):
	baseUrl = "../../"

	user = User.objects.get(id=key)
	if not (request.user.is_superuser or request.user == user):
		print user
		print request.user
		context = {'baseUrl' : baseUrl}	
		return render_to_response('denied.html', context, context_instance=RequestContext(request))
	
	if request.method == 'POST':
		form = PassWordChangeForm(request.POST)
		form.is_valid()

		con_user = authenticate(username=user.username, password = form.cleaned_data['oldpass'])
		if (con_user is not None) or request.user.is_superuser:
			newpass = form.cleaned_data['newpass1']
			if newpass == form.cleaned_data['newpass2']:
				user.set_password(newpass)
				user.save()
				context = { 'form': PassWordChangeForm(), 'baseUrl': baseUrl, 'message': "Password change successful"}
				return render_to_response('change_pass.html', context, context_instance=RequestContext(request))

		context = { 'form': PassWordChangeForm(), 'baseUrl': baseUrl, 'message': "Invalid input, please try again"}
		return render_to_response('change_pass.html', context, context_instance=RequestContext(request))
	
	else:
		form = PassWordChangeForm()
		context = { 'form': form, 'baseUrl': baseUrl }
		return render_to_response('change_pass.html', context, context_instance=RequestContext(request))
	
# Method for logging-out a user
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

# Method for retrieving a users profile details
def Profile(request):
	baseUrl = "../"

	if not request.user.is_authenticated():
		return HttpResponseRedirect(baseUrl + 'login/')
	
	if request.user.is_superuser:
		cons = Conference.objects.all()
	else:
		cons = Conference.objects.all().filter(user = request.user)
	context = {'con_user': request.user, 'cons': cons, 'baseUrl': baseUrl}
	return render_to_response('profile.html', context, context_instance=RequestContext(request))

# Method for retrieving a users profile details
def UserProfile(request, key):
	baseUrl = "../../"

	if not request.user.is_authenticated():
		return HttpResponseRedirect(baseUrl + 'login/')
	if not request.user.is_superuser:
		context = {'baseUrl' : baseUrl}	
		return render_to_response('denied.html', context, context_instance=RequestContext(request))

	user = ConAdmin.objects.get(pk=key)

	cons = Conference.objects.all().filter(user = user.user)
	context = {'con_user': user.user, 'cons': cons, 'baseUrl': baseUrl}
	return render_to_response('profile.html', context, context_instance=RequestContext(request))

# Method for banning users
def BanUser(request, key):
	baseUrl = "../../"

	if not request.user.is_superuser:
		context = {'baseUrl' : baseUrl}	
		return render_to_response('denied.html', context, context_instance=RequestContext(request))
	
	user = ConAdmin.objects.get(pk=key)
	[s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == user.user.id] # forces logout of all sessions
	user.user.is_active = False
	user.save()

	return HttpResponseRedirect(baseUrl+"manage_users/")

# Method for un-banning a user
def UnBanUser(request, key):
	baseUrl = "../../"

	if not request.user.is_superuser:
		context = {'baseUrl' : baseUrl}	
		return render_to_response('denied.html', context, context_instance=RequestContext(request))
	
	user = ConAdmin.objects.get(pk=key)
	user.user.is_active = True
	user.save()

	return HttpResponseRedirect(baseUrl+"manage_users/")

#M ethod for removing a user from the site
def DeleteUser(request, key):
	baseUrl = "../../"

	if not request.user.is_superuser:
		context = {'baseUrl' : baseUrl}	
		return render_to_response('denied.html', context, context_instance=RequestContext(request))
	
	user = ConAdmin.objects.get(pk=key)
	[s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == user.user.id] # forces logout of all sessions
	user.delete()

	return HttpResponseRedirect(baseUrl+"manage_users/")


# Method to return all users of the site
def ManageUsers(request):
	baseUrl = "../"

	if not request.user.is_superuser:
		context = {'baseUrl': baseUrl, 'message': 'You do not have permission to manage users'}
		return render_to_response('denied.html', context, context_instance=RequestContext(request))
	else:
		context = {'baseUrl': baseUrl, 'users': ConAdmin.objects.all() }
		return render_to_response('manage_users.html', context, context_instance=RequestContext(request))	
