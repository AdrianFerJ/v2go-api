from django.contrib import admin
from .models import User, EV, ChargingStation#, Driver, CSHost

class UserAdmin(admin.ModelAdmin):
    # display entries as table, with the following fields
    list_display = ('username', 'is_staff')


class ChargingStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'nk', 'address')


admin.site.register(User, UserAdmin)
admin.site.register(ChargingStation, ChargingStationAdmin)
admin.site.register(EV)
# admin.site.register(Driver)
# admin.site.register(CSHost)
