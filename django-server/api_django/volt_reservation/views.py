from .models import EventCS, EventEV
from main.models import ElectricVehicle as EV
from main.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .services import ReservationService
from .serializers import EventCSSerializer, EventEVSerializer
from django.utils import timezone
from datetime import datetime as dt
from main import constants
from django.http import Http404
import json
from datetime import datetime as dt


class EventCSView(viewsets.ReadOnlyModelViewSet):  
	""" Get's a32char nk and returns CS's detail info that matches the nk """
	lookup_field = 'nk'
	lookup_url_kwarg = 'cs_event_nk'
	today = timezone.now()

	queryset = EventCS.objects.all()
	serializer_class = EventCSSerializer

	def list(self, request, *args, **kwargs):
		if request.data == None:
			return super().list(request)
		else:
			start_datetime = dt.strptime(request.GET.get('start_datetime'), '%Y-%m-%d %H:%M:%S')
			end_datetime = dt.strptime(request.GET.get('end_datetime'), '%Y-%m-%d %H:%M:%S')

			queryset = ReservationService.get_available_event_cs(start_datetime, end_datetime)

			serializer = EventCSSerializer(queryset, many=True)

			return Response(serializer.data)


class EventEVView(viewsets.ModelViewSet):
	""" Get's a32char nk and returns CS's detail info that matches the nk """
	lookup_field = 'nk'
	lookup_url_kwarg = 'ev_event_nk'
	today = timezone.now()

	queryset = EventEV.objects.all()
	serializer_class = EventEVSerializer

	def create(self, request, *args, **kwargs):
		data = request.data

		# TODO: This should be handled by the permission
		# if request.user != ev.ev_owner:
			# return Response(None, status=status.HTTP_403_FORBIDDEN)

		try:
			event_cs = get_object_or_404(EventCS, nk=data.get('event_cs_nk'))
			ev = get_object_or_404(EV, nk=data.get('ev_nk'))

			event_ev = EventEV.objects.create(event_cs=event_cs, ev=ev)

			serializer = self.serializer_class(event_ev, many=False)

			return Response(serializer.data, status=status.HTTP_201_CREATED)
		except Http404:
			return Response(None, status=status.HTTP_404_NOT_FOUND)
		except:
			return Response(None, status=status.HTTP_400_BAD_REQUEST)

	@action(detail=False)
	def filter(self, request):
		user = request.user
		data = request.GET
		ev = get_object_or_404(EV, nk=data.get('vehicle_nk'))

		if ev.ev_owner != user:
			return Response(None, status=status.HTTP_403_FORBIDDEN)

		completed = ReservationService.get_completed_event_ev(ev, )

		serializer = self.serializer_class(completed, many=True)

		return Response(serializer.data)

	@action(detail=False)
	def custom(self, request):
		user = request.user
		data = request.GET
		event_cs = EventCS.objects.get(nk=data.get('event_cs_nk'))
		ev = EV.objects.get(nk=data.get('ev_nk'))

		custom_end_time = dt.strptime(data.get('custom_end_datetime'), '%Y-%m-%d %H:%M:%S')
		event_cs.change_end_datetime(custom_end_time)

		event_ev = EventEV.objects.create(event_cs=event_cs, ev=ev)

		serializer = self.serializer_class(event_ev, many=False)

		return Response(serializer.data, status=status.HTTP_201_CREATED)


	def retrieve(self, request, ev_event_nk=None):
		user = request.user
		event_ev = self.get_object()

		if event_ev.ev.ev_owner == user:
			serializer = self.serializer_class(event_ev, many=False)
			return Response(serializer.data)

		else:
			return Response(None, status=status.HTTP_400_BAD_REQUEST)

	def update(self, request, *args, **kwargs):
		event_ev = self.get_object()
		event_ev.status = constants.CANCELED
		event_ev.save()

		serializer = self.serializer_class(event_ev, many=False)
		return Response(serializer.data)
