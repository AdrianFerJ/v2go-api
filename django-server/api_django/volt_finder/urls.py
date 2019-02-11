from django.urls import re_path

from .apis import ChargingStationListView, ChargingStationDetailView

app_name = 'volt_finder'

urlpatterns = [
    re_path(r'^$', ChargingStationListView.as_view({'get': 'list'}), 
        name='cStations_list'),
    re_path(r'^(?P<cStation_nk>\w{32})/detail/$', ChargingStationDetailView.as_view(
        {'get': 'retrieve'}), name='cStation_detail'), 
]




