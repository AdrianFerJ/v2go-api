from .models import EventCS, EventEV
import datetime
from main import constants


class ReservationService(object):
	@staticmethod
	def get_completed_event_ev(ev):
		return EventEV.objects.filter(
			status=constants.COMPLETED,
			ev=ev
		)
