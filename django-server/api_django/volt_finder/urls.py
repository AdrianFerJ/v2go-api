from django.urls import re_path

from .apis import ChargingStationView

app_name = 'volt_finder'

urlpatterns = [
    re_path('', ChargingStationView.as_view({'get': 'list'}), name='cStations_list'),
]


