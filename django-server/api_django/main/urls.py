from django.urls import re_path, path
from rest_framework.urlpatterns import format_suffix_patterns
from main.views import ChargingStationList, ChargingStationDetail, EVList, EVDetail, \
                       SignUpView, LogInView, LogOutView


app_name = 'main'

urlpatterns = [
    path('stations', ChargingStationList.as_view(), name='cs_list'),
    path('stations/<nk>', ChargingStationDetail.as_view(),
        name='cs_detail'),
    path('sign-up', SignUpView.as_view(), name='sign_up'),
    path('login', LogInView.as_view(), name='log_in'),
    path('logout', LogOutView.as_view(), name='log_out'),
    # path('cs_hosts/', CSHostList.as_view(), name='cs_host_list'),
    # path('cs_hosts/<cs_host_nk>/', CSHostDetail.as_view(),
    #    name='host_cs_detail'),
    # path('ev_owners/', EVOwnerList.as_view(), name='ev_owner_list'),
    # path('ev_owners/<ev_owner_nk>', EVOwnerDetail.as_view(),
    #    name='ev_owner_detail'),
    path('vehicles/', EVList.as_view(), name='ev_list'),
    path('vehicle/<nk>', EVDetail.as_view(), name='ev_detail')
]
urlpatterns = format_suffix_patterns(urlpatterns)
