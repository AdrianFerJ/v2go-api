from .models import EventCS, EventEV
import datetime
from main import constants


class ReservationService(object):
	@staticmethod
	def get_event_cs_for_cs(cs_nk, start_date_time_range):
		return EventCS.objects.filter(
			cs__nk=cs_nk,
			startDateTime__range=start_date_time_range
		)

	@staticmethod
	def get_available_event_cs(start_date_time_range):
		return EventCS.objects.filter(
			startDateTime__range=start_date_time_range,
			status=constants.AVAILABLE
		)

	@staticmethod
	def get_completed_event_ev(ev):
		return EventEV.objects.filter(
			status=constants.COMPLETED,
			ev=ev
		)
