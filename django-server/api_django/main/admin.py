from django.contrib import admin
from .models import EV, EVOwner, ChargingStation, CSHost

admin.site.register(EV)
admin.site.register(EVOwner)
admin.site.register(ChargingStation)
admin.site.register(CSHost)
