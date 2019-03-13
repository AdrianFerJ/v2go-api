from django.urls import re_path, path

from .apis import ChargingStationListView, ChargingStationDetailView, ChargingStationTopNearListView

app_name = 'volt_finder'

urlpatterns = [
    re_path(r'^$', ChargingStationListView.as_view({'get': 'list'}), 
        name='cStations_list'),
    re_path(r'^(?P<cStation_nk>\w{32})/detail/$', ChargingStationDetailView.as_view(
        {'get': 'retrieve'}), name='cStation_detail'), 
    path('near_poi/<poi_location>/', ChargingStationTopNearListView.as_view(
        # {'get': 'list'}), name='cStations_near_poi'),
        {'get': 'top_cs_near_poi'}), name='cStations_near_poi'),
]




