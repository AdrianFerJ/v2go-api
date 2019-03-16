from .models import CSEvent, EVEvent
from rest_framework import viewsets
from rest_framework.response import Response
from .services import ReservationService
from .serializers import CSEventSerializer, EVEventSerializer
from django.utils import timezone
import datetime


class CSEventSerializerView(viewsets.ReadOnlyModelViewSet):  
	""" Get's a32char nk and returns CS's detail info that matches the nk """
	lookup_field = 'nk'
	lookup_url_kwarg = 'cs_event_nk'
	today = timezone.now()

	queryset = CSEvent.objects.all()
	serializer_class = CSEventSerializer

	def get_available_charging_station(self, request, datestr):
		#TODO: Implement a specified start and end time
		# 2017-12-20 03:26:53

		date = datetime.datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S').date()
		queryset = CSEvent.objects.filter(status='a', startDateTime__range=(date, date + datetime.timedelta(days=1)))

		serializer = CSEventSerializer(queryset, many=True)

		return Response(serializer.data)


class EVEventSerializerView(viewsets.ReadOnlyModelViewSet):
	""" Get's a32char nk and returns CS's detail info that matches the nk """
	lookup_field = 'nk'
	lookup_url_kwarg = 'ev_event_nk'
	today = timezone.now()

	queryset = EVEvent.objects.all()
	serializer_class = EVEventSerializer