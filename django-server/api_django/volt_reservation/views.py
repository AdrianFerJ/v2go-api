from .models import EventCS, EventEV
from main.models import ElectricVehicle as EV
from main.models import User
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from .services import ReservationService
from .serializers import EventCSSerializer, EventEVSerializer
from django.utils import timezone
from datetime import datetime as dt
from main import constants
import json


class EventCSView(viewsets.ReadOnlyModelViewSet):  
	""" Get's a32char nk and returns CS's detail info that matches the nk """
	lookup_field = 'nk'
	lookup_url_kwarg = 'cs_event_nk'
	today = timezone.now()

	queryset = EventCS.objects.all()
	serializer_class = EventCSSerializer

	def list(self, request):
		if request.data == None:
			return super().list(request)
		else:
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

			serializer = self.serializer_class(event_ev, many=False)

			return Response(serializer.data, status=status.HTTP_201_CREATED)
		except:
			return Response(None, status=status.HTTP_400_BAD_REQUEST)

	def get_completed_event_evs(self, request, vehicle_nk):
		user = request.user
		ev = EV.objects.get(nk=vehicle_nk)

		if ev.ev_owner != user:
			return Response(None, status=status.HTTP_403_FORBIDDEN)

		completed = ReservationService.get_completed_event_ev(ev)

		serializer = self.serializer_class(completed, many=True)

		return Response(serializer.data)

	def get_completed_event_detail(self, request, completed_nk):
		user = request.user
		event_ev = EventEV.objects.get(nk=completed_nk)

		if event_ev.ev.ev_owner == user:
			serializer = self.serializer_class(event_ev, many=False)
			return Response(serializer.data)

		else:
			return Response(None, status=status.HTTP_400_BAD_REQUEST)

	def cancel_event_ev(self, request, canceled_nk):
		user = request.user
		event_ev = EventEV.objects.get(nk=canceled_nk)
		event_ev.status = constants.CANCELED
		event_ev.save()

		serializer = self.serializer_class(event_ev, many=False)
		return Response(serializer.data)
