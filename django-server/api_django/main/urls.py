from django.urls import re_path, path
from rest_framework.urlpatterns import format_suffix_patterns
from main.views import ChargingStationList, ChargingStationDetail

app_name = 'main'

urlpatterns = [
    path('host/', ChargingStationList.as_view(), name='host_cs_list'),
    path('host/<cs_nk>/', ChargingStationDetail.as_view(),
        name='host_cs_detail'),
        
]
urlpatterns = format_suffix_patterns(urlpatterns)

#TODO review this, from reservation
# path('ev_owners', EVOwnerSerializerView.as_view({'get': 'list'}), name='ev_owners_list'),
# path('ev_cars', EVCarSerializerView.as_view({'get': 'list'}), name='ev_cars_list'),
# path('cs_owners', CSOwnerSerializerView.as_view({'get': 'list'}), name='cs_owners_list'),
# path('css', CSSerializerView.as_view({'get': 'list'}), name='css_list'),