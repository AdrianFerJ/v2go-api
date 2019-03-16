from django.urls import path

from .views import CSEventSerializerView, EVEventSerializerView

app_name = 'volt_reservation'

urlpatterns = [
	path('cs_events', CSEventSerializerView.as_view({'get': 'list'}), name='cs_events_list'),
	path('cs_events/available/<datestr>', CSEventSerializerView.as_view({'get': 'get_available_charging_station'}), name='available'),
	path('ev_events', EVEventSerializerView.as_view({'get': 'list'}), name='ev_events_list'),
]
