from .models import EventCS, EventEV
from datetime import datetime as dt
from main import constants


class ReservationService(object):
    @staticmethod
    def get_events_cs_for_cs(cs_nk, start_datetime, end_datetime):
        EventCS.objects.filter(cs__nk=cs_nk, end_datetime__lt=dt.now()).update(
            status=constants.COMPLETED)

        return EventCS.objects.filter(
            cs__nk=cs_nk,
            start_datetime__range=[start_datetime, end_datetime]
        )

    @staticmethod
    def get_available_events_cs(start_datetime, end_datetime):
        return EventCS.objects.filter(
            start_datetime__range=[start_datetime, end_datetime],
            status=constants.AVAILABLE
        )

    @staticmethod
    def get_completed_events_ev(ev):
        return EventEV.objects.filter(
            status=constants.COMPLETED,
            ev=ev
        )
