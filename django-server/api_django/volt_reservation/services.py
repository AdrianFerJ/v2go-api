from .models import EventCS
import datetime

class ReservationService(object):
	@staticmethod
	def get_available_event_cs(date):
		#TODO: Implement a specified start and end time
		return EventCS.objects.filter(
			status='AVAILABLE', startDateTime__range=(date, date + datetime.timedelta(days=1)))
