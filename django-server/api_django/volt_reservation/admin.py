from django.contrib import admin
from .models import EventCS, EventEV

class EventCSAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'cs', 'start_datetime', 'end_datetime' )
    ordering = ['id']
    exclude = ('nk', 'ev_event_id')
    search_fields = ['status', 'id']
    autocomplete_fields = ['cs']


class EventEVAdmin(admin.ModelAdmin):
    list_display = ('id', 'ev_owner', 'status' )
    ordering = ['id']
    exclude = ('nk', )
    search_fields = ['id', 'status']
    autocomplete_fields = ['ev_owner', 'event_cs', 'ev']


admin.site.register(EventEV, EventEVAdmin)
admin.site.register(EventCS, EventCSAdmin)
