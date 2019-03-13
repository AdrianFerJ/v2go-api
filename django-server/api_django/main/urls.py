from django.urls import re_path, path
from rest_framework.urlpatterns import format_suffix_patterns
from main.views import ChargingStationList, ChargingStationDetail

app_name = 'main'

urlpatterns = [
    path('host/', ChargingStationList.as_view(), name='host_cs_list'),
    
    # path('host/<cs_nk>/', ChargingStationDetail.as_view(
    #     {'get': 'retrieve'}), name='host_cs_detail'),
    
    # re_path(r'^host/(?P<cs_nk>\w{32})$', ChargingStationDetail.as_view(
    #     name='host_cs_detail')),
    # path('host/<str:cs_nk>', ChargingStationDetail.as_view(),
    # path('host/', ChargingStationDetail, {'cs_nk': 'cs_nk'},
    #     name='host_cs_detail')
    # path('host/<int:pk>/', ChargingStationDetail.as_view()),
    path('host/<cs_nk>/', ChargingStationDetail.as_view()),
        
]
urlpatterns = format_suffix_patterns(urlpatterns)

#TODO review this, from reservation
# path('ev_owners', EVOwnerSerializerView.as_view({'get': 'list'}), name='ev_owners_list'),
# path('ev_cars', EVCarSerializerView.as_view({'get': 'list'}), name='ev_cars_list'),
# path('cs_owners', CSOwnerSerializerView.as_view({'get': 'list'}), name='cs_owners_list'),
# path('css', CSSerializerView.as_view({'get': 'list'}), name='css_list'),