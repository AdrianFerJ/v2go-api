from django.urls import path

from .views import CSEventView, EVEventView

app_name = 'volt_reservation'

urlpatterns = [
	path('cs_events', CSEventView.as_view({'get': 'list'}), name='cs_events_list'),
	path('cs_events/available/<datestr>', CSEventView.as_view({'get': 'get_available_charging_station'}), name='available'),
	path('ev_events', EVEventView.as_view({'get': 'list'}), name='ev_events_list'),
]
