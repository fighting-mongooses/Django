from django.conf.urls import patterns, include, url
from django.contrib import admin
from con_user.models import ConAdmin
from con_user.forms import RegistrationForm
from conference.forms import ConferenceForm

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'androkon.views.home', name='home'),
    # url(r'^androkon/', include('androkon.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    (r'^register/$', 'con_user.views.ConAdminRegistration'),
    (r'^login/$', 'con_user.views.LoginRequest'),
    (r'^profile/$', 'con_user.views.Profile'),
    (r'^logout/$', 'con_user.views.LogoutRequest'),
    (r'^reg_con/$', 'conference.views.ConferenceRegistration'),
    (r'^edit_con/$', 'conference.views.ConferenceUpdate'),
    (r'^json_cons/$', 'conference.views.json_cons'),
    (r'^json_events/$', 'conference.views.json_events'),
)
