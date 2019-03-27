from .models import EventCS, EventEV
from rest_framework import viewsets
from rest_framework.response import Response
from .services import ReservationService
from .serializers import EventCSSerializer, EventEVSerializer
from django.utils import timezone
import datetime


class EventCSView(viewsets.ReadOnlyModelViewSet):  
	""" Get's a32char nk and returns CS's detail info that matches the nk """
	lookup_field = 'nk'
	lookup_url_kwarg = 'cs_event_nk'
	today = timezone.now()

	queryset = EventCS.objects.all()
	serializer_class = EventCSSerializer

	def get_available_charging_station(self, request, datestr):
		#TODO: Implement a specified start and end time
		# 2017-12-20 03:26:53

		date = datetime.datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S').date()
		queryset = EventCS.objects.filter(status='a', startDateTime__range=(date, date + datetime.timedelta(days=1)))

		serializer = EventCSSerializer(queryset, many=True)

		return Response(serializer.data)


class EventEVView(viewsets.ReadOnlyModelViewSet):
	""" Get's a32char nk and returns CS's detail info that matches the nk """
	lookup_field = 'nk'
	lookup_url_kwarg = 'ev_event_nk'
	today = timezone.now()

	queryset = EventEV.objects.all()
	serializer_class = EventEVSerializer
