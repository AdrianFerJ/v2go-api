from django.urls import re_path, path

from main import views #ChargingStationListView, ChargingStationDetailView, ChargingStationTopNearListView

app_name = 'main'

urlpatterns = [
    # path('host/', ChargingStationListView.as_view({'get': 'list'}), 
    #     name='host_cs_list'),
    path('host/', views.ChargingStationListView.as_view(), name='host_cs_list'),
]

#TODO review this, from reservation
# path('ev_owners', EVOwnerSerializerView.as_view({'get': 'list'}), name='ev_owners_list'),
# path('ev_cars', EVCarSerializerView.as_view({'get': 'list'}), name='ev_cars_list'),
# path('cs_owners', CSOwnerSerializerView.as_view({'get': 'list'}), name='cs_owners_list'),
# path('css', CSSerializerView.as_view({'get': 'list'}), name='css_list'),