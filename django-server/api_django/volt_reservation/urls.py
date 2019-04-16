from django.urls import path, include

from .views import EventCSView, EventEVView
from rest_framework.routers import DefaultRouter

app_name = 'volt_reservation'

router = DefaultRouter()
router.register(r'station-availabilities', EventCSView, 'station-availabilities')
router.register(r'reservations', EventEVView, 'reservations')

urlpatterns = [
	path('', include(router.urls)),

	path('reservations/completed/<vehicle_nk>',
		EventEVView.as_view({'get': 'get_completed_event_evs'}),
		name='completed_list'),

	path('reservations/completed/<completed_nk>/detail',
		EventEVView.as_view({'get': 'get_completed_event_detail'}),
		name='completed_event_detail'),
]
