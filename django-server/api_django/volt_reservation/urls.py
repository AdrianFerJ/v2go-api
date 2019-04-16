from django.urls import path, include

from .views import EventCSView, EventEVView
from rest_framework.routers import DefaultRouter

app_name = 'volt_reservation'

router = DefaultRouter()
router.register(r'station-availabilities', EventCSView, 'station-availabilities')

urlpatterns = [
	path('', include(router.urls)),

	path('reservations', EventEVView.as_view({'get': 'list'}), name='events_ev_list'),

	path('reservations/reserve',
		EventEVView.as_view({'post': 'post_reserve_available_charging_stations'}),
		name='reserve_cs'),

	path('reservations/completed/<vehicle_nk>',
		EventEVView.as_view({'get': 'get_completed_event_evs'}),
		name='completed_list'),

	path('reservations/completed/<completed_nk>/detail',
		EventEVView.as_view({'get': 'get_completed_event_detail'}),
		name='completed_event_detail'),

	path('reservations/cancel/<canceled_nk>',
		EventEVView.as_view({'put': 'cancel_event_ev'}),
		name='cancel_reservation')
]
