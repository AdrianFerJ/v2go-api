from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from main.serializers import ChargingStationSerializer #, UserSerializer, GeoCStationSerializer
from main.models import ChargingStation
from schedule.models import Calendar

class ChargingStationModelTest(APITestCase):
	def setUp(self):
		self.cs = ChargingStation.objects.create(
            address='1735 Rue Saint-Denis, Montréal, QC H2X 3K4, Canada', name='test_cs')
	
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
