from django.urls import re_path, path
from rest_framework.urlpatterns import format_suffix_patterns
from main.views import ChargingStationList, ChargingStationDetail

app_name = 'main'

urlpatterns = [
    path('cs/', ChargingStationList.as_view(), name='cs_list'),
    path('cs/<cs_nk>/', ChargingStationDetail.as_view(),
        name='cs_detail'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
