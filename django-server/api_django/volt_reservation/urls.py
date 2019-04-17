from django.urls import path, include

from .views import EventCSView, EventEVView
from rest_framework.routers import DefaultRouter

app_name = 'volt_reservation'

router = DefaultRouter()
router.register('station-availabilities', EventCSView, base_name='station-availabilities')
router.register('reservations', EventEVView, base_name='reservations')

urlpatterns = [
	path('', include(router.urls)),
]
