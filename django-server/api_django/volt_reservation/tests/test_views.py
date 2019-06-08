from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from main.serializers import ChargingStationSerializer
from main.models import ChargingStation
from main.models import ElectricVehicle as EV

from main import constants

from volt_reservation.models import EventCS, EventEV
from datetime import datetime as dt
from main import constants
from volt_reservation.services import ReservationService
import json
from utils.test_utils import create_user, cs_event_to_ordered_dict, filter_by_cs_event_nk


class TestEventCS(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cs_host = create_user()
        Group.objects.get_or_create(name=constants.U_OWNER)

        cls.cs_t1 = ChargingStation.objects.create( 
            name     = 'Panthere 1',
            address  = '1251 Rue Jeanne-Mance, Montréal, QC H2X, Canada', 
            lat      = 45.5070394,
            lng      = -73.5651293,
            cs_host  = cls.cs_host,
        )

        cls.cs_t2 = ChargingStation.objects.create( 
            name     = 'Panthere 2',
            address  = '1253 Rue Jeanne-Mance, Montréal, QC H2X, Canada', 
            lat      = 45.5210394,
            lng      = -73.543293,
            cs_host  = cls.cs_host,
        )


        cls.cs_event_1 = EventCS.objects.create(
        	startDateTime	= dt.strptime('2019-09-25 12:00:00', '%Y-%m-%d %H:%M:%S'),
			endDateTime		= dt.strptime('2019-09-25 12:30:00', '%Y-%m-%d %H:%M:%S'),
			cs 				= cls.cs_t1,
			status 			= constants.RESERVED,
            ev_event_id     = 1,
        )

        cls.cs_event_2 = EventCS.objects.create(
            startDateTime   = dt.strptime('2019-09-25 15:00:00', '%Y-%m-%d %H:%M:%S'),
            endDateTime     = dt.strptime('2019-09-25 15:30:00', '%Y-%m-%d %H:%M:%S'),
            cs              = cls.cs_t1,
            status          = constants.AVAILABLE
        )
 
        cls.cs_event_3 = EventCS.objects.create(
            startDateTime   = dt.strptime('2019-09-27 12:00:00', '%Y-%m-%d %H:%M:%S'),
            endDateTime     = dt.strptime('2019-09-27 12:30:00', '%Y-%m-%d %H:%M:%S'),
            cs              = cls.cs_t1,
            status          = constants.AVAILABLE
        )

        cls.cs_event_4 = EventCS.objects.create(
            startDateTime   = dt.strptime('2019-09-28 12:00:00', '%Y-%m-%d %H:%M:%S'),
            endDateTime     = dt.strptime('2019-09-28 12:30:00', '%Y-%m-%d %H:%M:%S'),
            cs              = cls.cs_t1,
            ev_event_id     = 1,
            status          = constants.RESERVED,
        )

        cls.cs_event_5 = EventCS.objects.create(
            startDateTime   = dt.strptime('2019-09-25 15:00:00', '%Y-%m-%d %H:%M:%S'),
            endDateTime     = dt.strptime('2019-09-25 17:30:00', '%Y-%m-%d %H:%M:%S'),
            cs              = cls.cs_t2,
            status          = constants.AVAILABLE
        )

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=self.cs_host.username, password=constants.PASSWORD)

    def test_host_can_filter_available_between_certain_time(self):
        response = self.client.get(reverse('volt_reservation:station-availabilities-list'), data={
            'startDateTime__range': ['2019-09-25 12:00:00', '2019-09-28 15:30:00'],
            'status': constants.AVAILABLE
        })
        
        result = response.data

        self.assertEqual(len(result), 3)
        self.assertFalse(filter_by_cs_event_nk(self.cs_event_1, result))
        self.assertTrue(filter_by_cs_event_nk(self.cs_event_2, result))
        self.assertTrue(filter_by_cs_event_nk(self.cs_event_3, result))
        self.assertFalse(filter_by_cs_event_nk(self.cs_event_4, result))
        self.assertTrue(filter_by_cs_event_nk(self.cs_event_5, result))

    def test_driver_can_get_weekly_availabilities(self):
        response = self.client.get(reverse('volt_reservation:station-availabilities-list'), data={
            'cs__nk': self.cs_t2.nk,
            'startDateTime__range': ['2019-09-25 12:00:00', '2019-09-28 15:30:00'],
            'status': constants.AVAILABLE
        })

        result = response.data

        self.assertEqual(len(result), 1)
        self.assertFalse(filter_by_cs_event_nk(self.cs_event_1, result))
        self.assertFalse(filter_by_cs_event_nk(self.cs_event_2, result))
        self.assertFalse(filter_by_cs_event_nk(self.cs_event_3, result))
        self.assertFalse(filter_by_cs_event_nk(self.cs_event_4, result))
        self.assertTrue(filter_by_cs_event_nk(self.cs_event_5, result))

class TestEventEV(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cs_host = create_user()
        Group.objects.get_or_create(name=constants.U_OWNER)
        # cls.cs_host.groups.add(Group.objects.get_or_create(name=U_OWNER))
        
        cls.cs_t1 = ChargingStation.objects.create( 
            name     = 'Panthere 1',
            address  = '1251 Rue Jeanne-Mance, Montréal, QC H2X, Canada', 
            lat      = 45.5070394,
            lng      = -73.5651293,
            cs_host  = cls.cs_host,
        )

        cls.cs_event_1 = EventCS.objects.create(
            startDateTime   = dt.strptime('2019-09-25 12:00:00', '%Y-%m-%d %H:%M:%S'),
            endDateTime     = dt.strptime('2019-09-25 12:30:00', '%Y-%m-%d %H:%M:%S'),
            cs              = cls.cs_t1,
            status          = constants.AVAILABLE
        )

        cls.cs_event_2 = EventCS.objects.create(
            startDateTime   = dt.strptime('2019-09-28 12:00:00', '%Y-%m-%d %H:%M:%S'),
            endDateTime     = dt.strptime('2019-09-28 12:30:00', '%Y-%m-%d %H:%M:%S'),
            cs              = cls.cs_t1,
            ev_event_id     = 1,
            status          = constants.RESERVED
        )

        cls.cs_event_3 = EventCS.objects.create(
            startDateTime   = dt.strptime('2019-09-27 12:00:00', '%Y-%m-%d %H:%M:%S'),
            endDateTime     = dt.strptime('2019-09-27 12:30:00', '%Y-%m-%d %H:%M:%S'),
            cs              = cls.cs_t1,
            status          = constants.AVAILABLE
        )

        cls.cs_event_4 = EventCS.objects.create(
            startDateTime   = dt.strptime('2019-09-29 12:00:00', '%Y-%m-%d %H:%M:%S'),
            endDateTime     = dt.strptime('2019-09-29 12:30:00', '%Y-%m-%d %H:%M:%S'),
            cs              = cls.cs_t1,
            status          = constants.AVAILABLE
        )

        cls.ev_driver = create_user(username='test@v2go.io')
        Group.objects.get_or_create(name=constants.U_DRIVER)

        cls.ev = EV.objects.create(
            model='Roadster',
            manufacturer='Tesla',
            year=2019,
            charger_type='A',
            ev_owner=cls.ev_driver
        )

        cls.completed_event_1 = EventEV.objects.create(
            status      = constants.COMPLETED,
            ev          = cls.ev,
            event_cs    = cls.cs_event_3
        )

    def setUp(self):
        self.client = APIClient()
        self.client.login(username=self.ev_driver.username, password=constants.PASSWORD) 

    def test_driver_can_reserve_available_charging_station(self):
        response = self.client.post(reverse('volt_reservation:reservations-list'), data={
            'event_cs_nk': self.cs_event_1.nk,
            'ev_nk': self.ev.nk
        })

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.cs_event_1.refresh_from_db()
        self.assertEqual(constants.RESERVED, self.cs_event_1.status)
        self.assertEqual(response.data['event_cs'], cs_event_to_ordered_dict(self.cs_event_1))
        self.assertEqual(response.data['ev'], self.ev.model)

    def test_driver_cannot_reserve_reserved_charging_station(self):
        response = self.client.post(reverse('volt_reservation:reservations-list'), data={
            'event_cs_nk': self.cs_event_2.nk,
            'ev_nk': self.ev.nk
        })

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_driver_can_view_completed_events_list(self):
        response = self.client.get(reverse('volt_reservation:reservations-filter'),
                                   data={'vehicle_nk': self.ev.nk})

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data[0]['event_cs'], cs_event_to_ordered_dict(self.cs_event_3))
        self.assertEqual(response.data[0]['ev'], self.ev.model)

    def test_driver_can_view_completed_event_detail(self):
        response = self.client.get(reverse('volt_reservation:reservations-detail',
                                   kwargs={'ev_event_nk': self.completed_event_1.nk}))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data['event_cs'], cs_event_to_ordered_dict(self.cs_event_3))
        self.assertEqual(response.data['ev'], self.ev.model)

    def test_driver_can_cancel_reservation(self):
        reserved = self.client.post(reverse('volt_reservation:reservations-list'), data={
            'event_cs_nk': self.cs_event_1.nk,
            'ev_nk': self.ev.nk
        })

        self.cs_event_1.refresh_from_db()

        self.assertEqual(reserved.data['event_cs'], cs_event_to_ordered_dict(self.cs_event_1))
        self.assertEqual(reserved.data['ev'], self.ev.model)
        self.assertEqual(self.cs_event_1.status, constants.RESERVED)
        self.assertTrue(self.cs_event_1.ev_event_id != -1)

        response = self.client.put(reverse('volt_reservation:reservations-detail',
                                          kwargs={'ev_event_nk': reserved.data['nk']}))

        self.cs_event_1.refresh_from_db()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.cs_event_1.status, constants.AVAILABLE)
        self.assertTrue(self.cs_event_1.ev_event_id == -1)


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