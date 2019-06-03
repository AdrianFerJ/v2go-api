from .models import EventCS, EventEV
import datetime
from main import constants


class ReservationService(object):
    @staticmethod
    def get_available_event_cs(start_datetime, end_datetime):
        return EventCS.objects.filter(
            status=constants.AVAILABLE,
            startDateTime__range=(start_datetime, end_datetime)
        )

    @staticmethod
    def get_completed_event_ev(ev):
        return EventEV.objects.filter(
            status=constants.COMPLETED,
            ev=ev
        )
