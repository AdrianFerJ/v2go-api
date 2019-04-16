from django.urls import path, include

from .views import EventCSView, EventEVView
from rest_framework.routers import DefaultRouter

app_name = 'volt_reservation'

router = DefaultRouter()
router.register(r'station-availabilities', EventCSView, 'station-availabilities')
router.register(r'reservations', EventEVView, 'reservations')

urlpatterns = [
	path('', include(router.urls)),
]
