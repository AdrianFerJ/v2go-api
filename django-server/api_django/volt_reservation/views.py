from .models import EventCS, EventEV
from rest_framework import viewsets
from rest_framework.response import Response
from .services import ReservationService
from .serializers import EventCSSerializer, EventEVSerializer
from django.utils import timezone
from datetime import datetime as dt
import json


class EventCSView(viewsets.ReadOnlyModelViewSet):  
	""" Get's a32char nk and returns CS's detail info that matches the nk """
	lookup_field = 'nk'
	lookup_url_kwarg = 'cs_event_nk'
	today = timezone.now()

	queryset = EventCS.objects.all()
	serializer_class = EventCSSerializer

	def get_available_charging_station(self, request):
		start_datetime = dt.strptime(request.GET.get('start_datetime'), '%Y-%m-%d %H:%M:%S')
		end_datetime = dt.strptime(request.GET.get('end_datetime'), '%Y-%m-%d %H:%M:%S')

		queryset = ReservationService.get_available_event_cs(start_datetime, end_datetime)

		serializer = EventCSSerializer(queryset, many=True)

		return Response(serializer.data)


class EventEVView(viewsets.ReadOnlyModelViewSet):
	""" Get's a32char nk and returns CS's detail info that matches the nk """
	lookup_field = 'nk'
	lookup_url_kwarg = 'ev_event_nk'
	today = timezone.now()

	queryset = EventEV.objects.all()
	serializer_class = EventEVSerializer
