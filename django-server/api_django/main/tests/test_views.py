from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from main.serializers import ChargingStationSerializer
from main.models import ChargingStation as CS, ElectricVehicle as EV
from volt_reservation.models import EventEV, EventCS
from schedule.models import Calendar
from main import constants
from datetime import datetime as dt
from utils.test_utils import filter_by_cs_event_nk, cs_event_to_ordered_dict, create_user, evs_to_ordered_dict, ev_event_to_ordered_dict
from django.contrib.auth.models import Group


""" TESTS """
class AuthenticationTest(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_user_can_sign_up(self):
        # photo_file = create_photo_file() #TODO: enable user photo
        response = self.client.post(reverse('main:sign_up'), data={
            'username'  : constants.USERNAME,
            'first_name': 'Test_name',
            'last_name' : 'Test_last',
            'password1' : constants.PASSWORD,
            'password2' : constants.PASSWORD,
            'group'     : 'driver',
            # 'photo': photo_file,
        })
        user = get_user_model().objects.last()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.data['id'], user.id)
        self.assertEqual(response.data['username'], user.username)
        self.assertEqual(response.data['first_name'], user.first_name)
        self.assertEqual(response.data['last_name'], user.last_name)
        # self.assertEqual(response.data['group'], user.group) #TODO: enable user gorup (driver or cs_owner)
        # self.assertIsNotNone(user.photo) #TODO: enable user photo ID

    def test_user_can_log_in(self):
        user = create_user()
        response = self.client.post(reverse('main:log_in'), data={
            'username': user.username,
            'password': constants.PASSWORD,
        })
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data['username'], user.username)

    def test_user_can_log_out(self):
        user = create_user()
        self.client.login(username=user.username, password=constants.PASSWORD)
        response = self.client.post(reverse('main:log_out'))
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    # def test_annon_user_can_not_retrive_cs_detail(self):
    #     """ Attempt to access endpoints that require login as annon user (no-login) """
    #     host = create_user()
    #     cs = CS.objects.create(
    #         address='1735 Rue Saint-Denis, Montréal, QC H2X 3K4, Canada',
    #         name='test_cs',
    #         cs_host  = host,
    #     )

    #     response = self.client.get(cs.get_absolute_url())
    #     self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    # def test_annon_user_can_not_retrive_cs_list(self):
    #     """ Attempt to access endpoints that require login as annon user (no-login) """
    #     response = self.client.get(reverse('main:stations-list'))
    #     self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)


class UserTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cs_host = create_user()
        cls.user = create_user(username='driver')
        Group.objects.get_or_create(name=constants.U_DRIVER)
        Group.objects.get_or_create(name=constants.U_OWNER)

        cls.cs_t1 = CS.objects.create(
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
            status          = constants.COMPLETED
        )

        cls.ev = EV.objects.create(
            model='Roadster',
            manufacturer='Tesla',
            year=2019,
            charger_type='A',
            ev_owner=cls.user
        )

        cls.reserved_event = EventEV.objects.create(
            status      = constants.RESERVED,
            ev          = cls.ev,
            event_cs    = cls.cs_event_1,
            ev_owner    = cls.user
        )

        cls.completed_event = EventEV.objects.create(
            status      = constants.COMPLETED,
            ev          = cls.ev,
            event_cs    = cls.cs_event_2,
            ev_owner    = cls.user
        )

    def setUp(self):
        self.client = APIClient()

    def test_user_view_my_account(self):
        """User attempts to view their account info"""
        self.client.login(username=self.user.username, password=constants.PASSWORD)

        response = self.client.get(reverse('main:my_account', kwargs={'user_id': self.user.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data.get('user'), {
            'id'        : self.user.id,
            'username'  : self.user.username,
            'first_name': self.user.first_name,
            'last_name' : self.user.last_name,
        })

        self.assertEqual(response.data.get('evs'), evs_to_ordered_dict([self.ev]))
        self.assertEqual(response.data.get('reservations'), ev_event_to_ordered_dict([self.reserved_event, self.completed_event]))


class DriverVehicleTest(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.login(username=self.user.username, password=constants.PASSWORD)

    def test_driver_can_create_vehicle(self):
        response = self.client.post(reverse('main:vehicles-list'), data={
            'model'         : 'Roadster',
            'manufacturer'  : 'Tesla',
            'year'          : 2019,
            'ev_owner'      : self.user.pk,
        })

        new_ev = EV.objects.all().latest('id')
        calendar = Calendar.objects.all().latest('id')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(new_ev.model, response.data.get('model'))
        self.assertEqual(calendar.id, response.data.get('calendar'))


class HostChargingStationTest(APITestCase):
    """ Test all Model-backed API views for CS (only available for cs Owner
        # TODO setUp() should create user with group=U_OWNER)
        # TODO Add 2 tests for host can't retrive cs owned by another host (cs_list AND cs_detail)
        # TODO host can update cs
        # TODO host can delete cs
    """

    def setUp(self):
        user = create_user()  # group=U_OWNER)
        self.client = APIClient()
        self.client.login(username=user.username, password=constants.PASSWORD)

    @classmethod
    def setUpTestData(cls):
        host = create_user(username='host')
        cls.cs_t1 = CS.objects.create(
            name    = 'Panthere 1',
            address = '1251 Rue Jeanne-Mance, Montréal, QC H2X, Canada',
            lat     = 45.5070394,
            lng     = -73.5651293,
            cs_host = host
        )
        cls.cs_t2 = CS.objects.create(
            name    = 'Panthere 2',
            address = '1251 Rue Jeanne-Mance, Montréal, QC H2X, Canada',
            lat     = 45.5070394,
            lng     = -73.5651293,
            cs_host = host
        )

    def test_host_can_retrive_her_cs_list(self):
        """ Get CS list
            # TODO: should display only CS created by group=U_OWNER)
        """
        response = self.client.get(reverse('main:stations-list'))
        exp_cs_nks = [self.cs_t1.nk, self.cs_t2.nk]
        act_cs_nks = [cs.get('nk') for cs in response.data]
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertCountEqual(exp_cs_nks, act_cs_nks)

    def test_host_can_retrieve_cs_detail_by_nk(self):
        response = self.client.get(self.cs_t1.get_absolute_url())
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.cs_t1.nk, response.data.get('nk'))

    def test_host_can_create_cs(self):
        test_host = create_user(username='test_host')
        response = self.client.post(reverse('main:stations-list'), data={
            'name'      : 'Panthere_Host_Created',
            'address'   : '1251 Rue Jeanne-Mance, Montréal, QC H2X, Canada',
            'lat'       : 45.5070394,
            'lng'       : -70.5070394,
            'cs_host'   : test_host.pk
        })

        new_cs = CS.objects.all().latest('id')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(new_cs.name, response.data.get('name'))
