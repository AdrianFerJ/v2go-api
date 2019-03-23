from .models import CSEvent
import datetime

class ReservationService(object):
	@staticmethod
	def get_available_cs_event(date):
		#TODO: Implement a specified start and end time
		return CSEvent.objects.filter(
			status='AVAILABLE', startDateTime__range=(date, date + datetime.timedelta(days=1)))
