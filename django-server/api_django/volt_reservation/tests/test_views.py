from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from main.serializers import ChargingStationSerializer #, UserSerializer, GeoCStationSerializer
from main.models import ChargingStation
from volt_reservation.models import EventCS
from datetime import datetime as dt
from volt_reservation.services import ReservationService


""" HELPER FUNC """
PASSWORD = 'pAssw0rd?XD'
USERNAME = 'user@example.com'
U_DRIVER = 'EV_DRIVER'
U_OWNER  = 'CS_HOST'

def create_user(username=USERNAME, password=PASSWORD):
    return get_user_model().objects.create_user(
        username=username, password=password)


class TestEventCS(APITestCase):
    def setUp(self):
        self.cs_host = create_user()
        Group.objects.get_or_create(name=U_OWNER)
        # self.cs_host.groups.add(Group.objects.get_or_create(name=U_OWNER))
        self.client = APIClient()
        self.client.login(username=self.cs_host.username, password=PASSWORD)   

        self.cs_t1 = ChargingStation.objects.create( 
            name     = 'Panthere 1',
            address  = '1251 Rue Jeanne-Mance, Montréal, QC H2X, Canada', 
            lat      = 45.5070394,
            lng      = -73.5651293,
            cs_host  = self.cs_host,
        )

        self.cs_event_1 = EventCS.objects.create(
        	startDateTime	= dt.strptime('2019-09-25 12:00:00', '%Y-%m-%d %H:%M:%S'),
			endDateTime		= dt.strptime('2019-09-25 12:30:00', '%Y-%m-%d %H:%M:%S'),
			cs 				= self.cs_t1,
			status 			= 'RESERVED'
        )

        self.cs_event_2 = EventCS.objects.create(
            startDateTime   = dt.strptime('2019-09-25 15:00:00', '%Y-%m-%d %H:%M:%S'),
            endDateTime     = dt.strptime('2019-09-25 15:30:00', '%Y-%m-%d %H:%M:%S'),
            cs              = self.cs_t1,
            status          = 'AVAILABLE'
        )
 
        self.cs_event_3 = EventCS.objects.create(
            startDateTime   = dt.strptime('2019-09-27 12:00:00', '%Y-%m-%d %H:%M:%S'),
            endDateTime     = dt.strptime('2019-09-27 12:30:00', '%Y-%m-%d %H:%M:%S'),
            cs              = self.cs_t1,
            status          = 'AVAILABLE'
        )

        self.cs_event_4 = EventCS.objects.create(
            startDateTime   = dt.strptime('2019-09-28 12:00:00', '%Y-%m-%d %H:%M:%S'),
            endDateTime     = dt.strptime('2019-09-28 12:30:00', '%Y-%m-%d %H:%M:%S'),
            cs              = self.cs_t1,
            status          = 'RESERVED'
        )

    def test_host_can_retrive_her_cs_list(self):
        """ Get CS list
            #TODO: should display only CS created by group=U_OWNER)
        """
        response = self.client.get(reverse('volt_reservation:available', kwargs={'datestr': '2019-09-25 12:00:00'}))
        print(response.data)

    def test_host_can_filter_available_between_certain_time(self):
        startDateTime   = dt.strptime('2019-09-25 11:00:00', '%Y-%m-%d %H:%M:%S')
        endDateTime     = dt.strptime('2019-09-28 15:30:00', '%Y-%m-%d %H:%M:%S')
        result = ReservationService.get_available_event_cs(startDateTime, endDateTime)

        self.assertEqual(len(result), 2)
        self.assertTrue(self.cs_event_1 not in result)
        self.assertTrue(self.cs_event_2 in result)
        self.assertTrue(self.cs_event_3 in result)
        self.assertTrue(self.cs_event_4 not in result)

    # def test_host_can_retrieve_cs_detail_by_nk(self):
    #     response = self.client.get(self.cs_t1.get_absolute_url())
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     self.assertEqual(self.cs_t1.nk, response.data.get('nk'))











# class AuthenticationTest(APITestCase):

#     def setUp(self):
#         self.client = APIClient()



#             def test_annon_user_can_not_retrive_cs_detail(self):
#         """ Attempt to access endpoints that require login as annon user (no-login) """
#         cs = ChargingStation.objects.create(
#             address='1735 Rue Saint-Denis, Montréal, QC H2X 3K4, Canada', name='test_cs')
#         response = self.client.get(cs.get_absolute_url())
#         self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
    
#     def test_annon_user_can_not_retrive_cs_list(self):
#         """ Attempt to access endpoints that require login as annon user (no-login) """
#         response = self.client.get(reverse('main:cs_list'))
#         self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)