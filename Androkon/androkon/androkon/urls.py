from django.conf.urls import patterns, include, url
from django.contrib import admin
from con_user.models import ConAdmin
from con_user.forms import RegistrationForm
from conference.forms import ConferenceForm
from django.http import HttpResponseRedirect
import random

admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'androkon.views.home', name='home'),
	# url(r'^androkon/', include('androkon.foo.urls')),
	
	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	url(r'^admin/', include(admin.site.urls)),
	(r'^$', lambda r : HttpResponseRedirect('profile/')),
	(r'^invite/$', lambda r : HttpResponseRedirect('../invite/0')),
	(r'^invite/(?P<msg>\d+)/$', 'con_user.views.Invite'),
	(r'^invite/new/$', lambda r : HttpResponseRedirect('../../invite/new/0')),
	(r'^invite/new/(?P<key>\d+)/$', 'con_user.views.NewInvite'),
	(r'^invite/delete/(?P<key>\d+)/$', 'con_user.views.DeleteInvite'),
	(r'^register/$', lambda r : HttpResponseRedirect('../register/0')),
	(r'^register/(?P<key>\d+)/$', 'con_user.views.ConAdminRegistration'),
	(r'^login/$', 'con_user.views.LoginRequest'),
	(r'^profile/$', 'con_user.views.Profile'),
	(r'^logout/$', 'con_user.views.LogoutRequest'),
	(r'^reg_con/$', 'conference.views.ConferenceRegistration'),
	(r'^edit_con/(?P<key>\d+)$', 'conference.views.ConferenceUpdate'),
	(r'^delete_con/(?P<key>\d+)/$', 'conference.views.DeleteCon'),
	(r'^restore_con/(?P<key>\d+)/$', 'conference.views.RestoreCon'),
	(r'^manage_events/(?P<key>\d+)/$', 'conference.views.ManageEvents'),
	(r'^add_event/(?P<key>\d+)/$', 'conference.views.AddEvent'),
	(r'^edit_event/(?P<key>\d+)/$', 'conference.views.EditEvent'),
	(r'^delete_event/(?P<key>\d+)/$', 'conference.views.DeleteEvent'),
	(r'^restore_event/(?P<key>\d+)/$', 'conference.views.RestoreEvent'),
	(r'^json_cons/$', 'conference.views.json_cons'),
	(r'^json_events/$', 'conference.views.json_events'),
	(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/img/favicon.ico'}),
    (r'^resetpassword/passwordsent/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^resetpassword/$', 'django.contrib.auth.views.password_reset'),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
	)
