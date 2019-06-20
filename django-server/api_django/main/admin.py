from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import User, ChargingStation
from .models import ElectricVehicle as EV


class V2GoUserAdmin(UserAdmin):
    # display entries as table, with the following fields
    list_display = ('pk', 'username', 'is_staff')
    ordering = ['pk']
    search_fields = ['username', 'pk']


class ChargingStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk', 'nk', 'address')
    exclude = ('calendar', 'nk')
    ordering = ['name']
    search_fields = ['name', 'pk']
    autocomplete_fields = ['cs_host']


class EVAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'ev_owner', 'pk', 'model', 'manufacturer')
    ordering = ['pk']
    exclude = ('calendar', 'nk')
    search_fields = ['nickname', 'model']
    autocomplete_fields = ['ev_owner']


admin.site.register(User, V2GoUserAdmin)
admin.site.register(ChargingStation, ChargingStationAdmin)
admin.site.register(EV, EVAdmin)
# admin.site.register(Driver)
# admin.site.register(CSHost)
