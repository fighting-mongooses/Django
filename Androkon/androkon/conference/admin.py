from django.contrib import admin
from conference.models import Conference, Event


class EventInline(admin.StackedInline):
	prepopulated_fileds = {'slug': ('name'),}
	model = Event
	extra = 3


class ConferenceAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['name', 'description']}),
		('Date information', {'fields': ['start_date', 'end_date']}),
		('User', {'fields': ['user']}),
	]
	inlines	= [EventInline]

admin.site.register(Conference, ConferenceAdmin)