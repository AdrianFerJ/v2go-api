from django.contrib import admin
from .models import EV, Driver, ChargingStation, CSHost

admin.site.register(EV)
admin.site.register(Driver)
admin.site.register(ChargingStation)
admin.site.register(CSHost)
