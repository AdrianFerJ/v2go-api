from django.urls import path, include

from .views import ChargingStationTopNearListView
from rest_framework.routers import DefaultRouter

app_name = 'volt_finder'

router = DefaultRouter()
router.register('near-poi', ChargingStationTopNearListView, base_name='near-poi')


urlpatterns = [
    path('', include(router.urls))
]
