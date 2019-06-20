from django.contrib import admin
from .models import EventCS, EventEV

class EventCSAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'cs', 'start_datetime', 'end_datetime' )


class EventEVAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'ev_owner', )


admin.site.register(EventEV, EventEVAdmin)
admin.site.register(EventCS, EventCSAdmin)
