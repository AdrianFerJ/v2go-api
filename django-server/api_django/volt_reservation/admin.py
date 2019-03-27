from django.contrib import admin
from .models import CSEvent, EVEvent


admin.site.register(EVEvent)
admin.site.register(CSEvent)
