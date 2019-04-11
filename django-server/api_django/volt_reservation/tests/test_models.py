from rest_framework.test import APIClient, APITestCase
from rest_framework.serializers import ValidationError
from django.contrib.auth import get_user_model
from volt_reservation.models import EventEV, EventCS
from main.models import ChargingStation

from django.utils import timezone 
import datetime as dt

""" HELPER FUNC """
PASSWORD = 'pAssw0rd?XD'
USERNAME = 'user@example.com'
U_OWNER  = 'CS_HOST'

def create_user(username=USERNAME, password=PASSWORD):
    return get_user_model().objects.create_user(
        username=username, password=password)


""" TESTS """
class EventCSTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        host = create_user()
        cls.cs = ChargingStation.objects.create( 
            name     = 'Panthere 1',
            address  = '1251 Rue Jeanne-Mance, Montréal, QC H2X, Canada', 
            lat      = 45.5070394,
            lng      = -73.5651293,
            cs_host  = host
        )
        
        cls.start_time = dt.datetime.now()
        cls.end_time = cls.start_time + dt.timedelta(minutes=30)
        cls.event_cs = EventCS.objects.create(
            startDateTime	= cls.start_time,
            endDateTime	    = cls.end_time,
            cs 			    = cls.cs
        )

    def test_same_date_cs(self):
        self.assertRaises(ValidationError,  EventCS.objects.create, 
            startDateTime=self.start_time,
            endDateTime=self.end_time,
            cs=self.cs
        )
