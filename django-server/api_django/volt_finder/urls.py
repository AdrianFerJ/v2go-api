from django.urls import re_path, path

from .views import ChargingStationTopNearListView

app_name = 'volt_finder'

urlpatterns = [
    path('near_poi/<poi_location>/', ChargingStationTopNearListView.as_view(
        {'get': 'top_cs_near_poi'}), name='cs_near_poi'),
]




