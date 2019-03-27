from django.urls import re_path, path

from .views import ChargingStationTopNearListView

app_name = 'volt_finder'

urlpatterns = [
    path('near_poi/<poi_location>/', ChargingStationTopNearListView.as_view(
        {'get': 'get_top_cs_near_poi_no_date'}), name='cs_near_poi_status_any'),
    path('near_poi/<poi_location>/<date_x>/', ChargingStationTopNearListView.as_view(
        {'get': 'get_top_cs_near_poi_available_date'}), name='cs_near_poi_status_avail_today'),
]




