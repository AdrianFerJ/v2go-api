from django.urls import re_path, path
from rest_framework.urlpatterns import format_suffix_patterns
from main.views import ChargingStationList, ChargingStationDetail, CSHostList, CSHostDetail, \
					   EVOwnerList, EVOwnerDetail, EVList, EVDetail

app_name = 'main'

urlpatterns = [
    path('cs/', ChargingStationList.as_view(), name='cs_list'),
    path('cs/<cs_nk>/', ChargingStationDetail.as_view(),
        name='cs_detail'),
    path('cs_hosts/', CSHostList.as_view(), name='cs_host_list'),
    path('cs_hosts/<cs_host_nk>/', CSHostDetail.as_view(),
    	name='host_cs_detail'),
    path('ev_owners/', EVOwnerList.as_view(), name='ev_owner_list'),
    path('ev_owners/<ev_owner_nk>', EVOwnerDetail.as_view(),
    	name='ev_owner_detail'),
    path('ev/', EVList.as_view(), name='ev_list'),
    path('ev/<ev_nk>', EVDetail.as_view(), name='ev_detail')
]
urlpatterns = format_suffix_patterns(urlpatterns)
