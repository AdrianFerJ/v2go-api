from django.urls import path

from .views import EventCSView, EventEVView

app_name = 'volt_reservation'

urlpatterns = [
	path('station-availabilities', EventCSView.as_view({'get': 'list'}), name='events_cs_list'),
	path('station-availabilities/vacant', EventCSView.as_view({'get': 'get_available_charging_station'}), name='available'),
	path('reservations', EventEVView.as_view({'get': 'list'}), name='events_ev_list'),

	path('reservations/reserve',
		EventEVView.as_view({'post': 'post_reserve_available_charging_stations'}),
		name='reserve_cs'),

	path('reservations/completed/<ev_nk>',
		EventEVView.as_view({'get': 'get_completed_event_evs'}),
		name='completed_list'),

	path('reservations/completed/<event_ev_nk>/detail',
		EventEVView.as_view({'get': 'get_completed_event_detail'}),
		name='completed_event_detail'),

	path('reservations/cancel/<nk>', EventEVView.as_view({'put': 'cancel_event_ev'}), name='cancel_reservation')
]
