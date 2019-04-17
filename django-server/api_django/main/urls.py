from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from main.views import ChargingStationViewSet, EVList, EVDetail, \
                       SignUpView, LogInView, LogOutView
from rest_framework.routers import DefaultRouter


app_name = 'main'

router = DefaultRouter()
router.register(r'stations', ChargingStationViewSet, 'stations')


urlpatterns = [
    path('', include(router.urls)),
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
    path('vehicles/<vehicle_nk>', EVDetail.as_view(), name='ev_detail')
]