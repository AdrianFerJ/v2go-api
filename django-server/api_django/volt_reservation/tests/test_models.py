from rest_framework.test import APIClient, APITestCase
from rest_framework.serializers import ValidationError

from volt_reservation.models import EventEV, EventCS
from main.models import ChargingStation

from django.utils import timezone 
import datetime as dt


""" TESTS """
class EventCSTest(APITestCase):
    def setUp(self):
        self.cs = ChargingStation.objects.create( 
            name     = 'Panthere 1',
            address  = '1251 Rue Jeanne-Mance, Montréal, QC H2X, Canada', 
            lat      = 45.5070394,
            lng      = -73.5651293
        )
        
        self.start_time = dt.datetime.now()
        self.end_time = self.start_time + dt.timedelta(minutes=30)
        self.event_cs = EventCS.objects.create(
            startDateTime	= self.start_time,
            endDateTime	    = self.end_time,
            cs 			    = self.cs
        )

    def test_same_date_cs(self):
        self.assertRaises(ValidationError, EventCS.objects.create, 
            startDateTime=self.start_time,
            endDateTime=self.end_time,
            cs=self.cs
        )
