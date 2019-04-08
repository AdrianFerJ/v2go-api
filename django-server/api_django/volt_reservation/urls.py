from django.urls import path

from .views import EventCSView, EventEVView

app_name = 'volt_reservation'

urlpatterns = [
	path('events_cs', EventCSView.as_view({'get': 'list'}), name='events_cs_list'),
	path('events_cs/available/', EventCSView.as_view({'get': 'get_available_charging_station'}), name='available'),
	path('events_ev', EventEVView.as_view({'get': 'list'}), name='events_ev_list'),
	
	path('events_ev/reserve', EventEVView.as_view(
        {'post': 'post_reserve_available_charging_stations'}), name='reserve_cs'),
	path('events_ev/completed', EventEVView.as_view({'get': 'get_completed_event_evs'}), name='completed_list'),
	path('events_ev/completed/<nk>', EventEVView.as_view({'get': 'get_completed_event_ev'}), name='completed_event')
]
