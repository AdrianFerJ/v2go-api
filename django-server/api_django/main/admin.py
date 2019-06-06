from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import User, ChargingStation
from .models import ElectricVehicle as EV


class V2GoUserAdmin(UserAdmin):
    # display entries as table, with the following fields
    list_display = ('username', 'is_staff')


class ChargingStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'nk', 'address')


admin.site.register(User, V2GoUserAdmin)
admin.site.register(ChargingStation, ChargingStationAdmin)
admin.site.register(EV)
# admin.site.register(Driver)
# admin.site.register(CSHost)
