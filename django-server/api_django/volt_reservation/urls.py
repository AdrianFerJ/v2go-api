from django.urls import path

from .views import EventCSView, EventEVView

app_name = 'volt_reservation'

urlpatterns = [
	path('events_cs', EventCSView.as_view({'get': 'list'}), name='events_cs_list'),
	path('events_cs/available/', EventCSView.as_view({'get': 'get_available_charging_station'}), name='available'),
	path('events_ev', EventEVView.as_view({'get': 'list'}), name='events_ev_list'),
	path('events_ev/reserve', EventEVView.as_view(
        {'post': 'post_reserve_available_charging_stations'}), name='reserve_cs')
]
