from .models import EventCS, EventEV
import datetime

class ReservationService(object):
	@staticmethod
	def get_available_event_cs(start_datetime, end_datetime):
		return EventCS.objects.filter(
			status='AVAILABLE',
			startDateTime__range=(start_date, end_date)
		)

	@staticmethod
	def get_completed_event_ev(ev):
		return EventEV.objects.filter(
			status='COMPLETED',
			ev=ev
		)
