from .models import EventCS
import datetime

class ReservationService(object):
	@staticmethod
	def get_available_event_cs(start_date, end_date):
		return EventCS.objects.filter(
			status='AVAILABLE', startDateTime__range=(start_date, end_date))
