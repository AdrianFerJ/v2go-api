from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import Group

from main.serializers import ChargingStationSerializer #, UserSerializer, GeoCStationSerializer
from main.models import ChargingStation
from schedule.models import Calendar

""" HELPER FUNC """
PASSWORD = 'pAssw0rd?XD'
USERNAME = 'user@example.com'
U_OWNER  = 'CS_HOST'

def create_user(username=USERNAME, password=PASSWORD):
    return get_user_model().objects.create_user(
        username=username, password=password)


class ChargingStationModelTest(APITestCase):
    def setUp(self):
        self.cs_host = create_user()
        self.client = APIClient()
        self.client.login(username=self.cs_host.username, password=PASSWORD)   

        self.cs = ChargingStation.objects.create( 
            name     = 'Panthere 1',
            address  = '1251 Rue Jeanne-Mance, Montréal, QC H2X, Canada', 
            lat      = 45.5070394,
            lng      = -73.5651293,
            cs_host  = self.cs_host,
        )
	
    def test_calendar_linked_to_cs_is_deleted_with_cs(self):
        """Test deleting Charging Stations"""
        cal = self.cs.calendar
        self.assertEqual(Calendar.objects.filter(id=cal.id).exists(), True)
        self.cs.delete()
        self.assertEqual(Calendar.objects.filter(id=cal.id).exists(), False)

# Missing tests for ChargingStation
#TODO require mandatory fields, fail if not provided
#TODO get_absolute_url
#TODO create_geo_location
#TODO save() *If no nk, if nk, if no geo_locatoin, if geo_location
