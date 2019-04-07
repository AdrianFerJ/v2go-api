from .models import EventCS, EventEV
<<<<<<< HEAD
from main.models import ElectricVehicle as EV
=======
from main.models import EV
>>>>>>> Reserve available charging station with response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from .services import ReservationService
from .serializers import EventCSSerializer, EventEVSerializer
from django.utils import timezone
<<<<<<< HEAD
from datetime import datetime as dt
import json
=======
from rest_framework.response import Response
from main.models import User
import datetime

>>>>>>> Reserve available charging station with response

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

	def post_reserve_available_charging_stations(self, request):
		data = request.data
		event_cs = EventCS.objects.get(nk=data['event_cs_nk'])
		ev = EV.objects.get(nk=data['ev_nk'])

		# TODO: This should be handled by the permission
		# if request.user != ev.ev_owner:
			# return Response(None, status=status.HTTP_403_FORBIDDEN)

		try:
			event_ev = EventEV.objects.create(event_cs=event_cs, ev=ev)

			serializer = EventEVSerializer(event_ev, many=False)

			return Response(serializer.data, status=status.HTTP_201_CREATED)
		except:
			return Response(None, status=status.HTTP_400_BAD_REQUEST)

	def get_completed_event_evs(self, request):
		user = request.user
		evs = EV.objects.filter(ev_owner=user)

		completed = None

		for ev in evs:
			if completed is None:
				completed = ReservationService.get_completed_event_ev(ev)
			else:
				completed = completed | ReservationService.get_completed_event_ev(ev)

		serializer = EventEVSerializer(completed, many=True)

		return Response(serializer.data)

