from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase


from volt_finder.serializers import CStationSerializer, UserSerializer
from volt_finder.models import ChargingStation

PASSWORD = 'pAssw0rd!'

""" HELPER FUNC """
def create_user(username='user@example.com', password=PASSWORD): # new
    return get_user_model().objects.create_user(
        username=username, password=password)


""" TESTS """

class AuthenticationTest(APITestCase):

    def setUp(self):
        self.client = APIClient()

    # Function collapsed for clarity.
    def test_user_can_sign_up(self): ...

    def test_user_can_log_in(self): # new
        user = create_user()
        response = self.client.post(reverse('log_in'), data={
            'username': user.username,
            'password': PASSWORD,
        })
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data['username'], user.username)

    def test_user_can_log_out(self): # new
        user = create_user()
        self.client.login(username=user.username, password=PASSWORD)
        response = self.client.post(reverse('log_out'))
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

class HttpCSFinderTest(APITestCase):
    """ Tests the ability to get the (single) nearest CS to user provided POI""" 

    def setUp(self):
        user = create_user()
        self.client = APIClient()
        self.client.login(username=user.username, password=PASSWORD)


    def test_get_list_of_cs_near_poi(self):
        cStations = [
            ChargingStation.objects.create(location='160 Rue Saint Viateur E, Montréal, QC H2T 1A8', name='Panthere 1'),
            ChargingStation.objects.create(location='1735 Rue Saint-Denis, Montréal, QC H2X 3K4', name='Panthere 2'),
            ChargingStation.objects.create(location='2153 Mackay St, Montreal, QC H3G 2J2', name='Panthere 3'),
        ]      

        response = self.client.get(reverse('trip:cStations_list'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # expected and actual nks
        exp_trip_nks = [cs.nk for cs in cStations]
        act_trip_nks = [cs.get('nk') for cs in response.data]
        self.assertCountEqual(exp_trip_nks, act_trip_nks)


    #TODO: def test_find_single_nearest_cs_to_poi(self):
    #   user_poi_location = '969 Rachel St E, Montreal, QC H2J 2J2'

    # def test_user_can_list_trips(self):
    #     trips = [
    #         Trip.objects.create(pick_up_address='A', drop_off_address='B'),
    #         Trip.objects.create(pick_up_address='B', drop_off_address='C')
    #     ]
    #     response = self.client.get(reverse('trip:trip_list'))
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     exp_trip_nks = [trip.nk for trip in trips]
    #     act_trip_nks = [trip.get('nk') for trip in response.data]
    #     self.assertCountEqual(exp_trip_nks, act_trip_nks)

      # panthereLocations = [,
        #    "145 Mont-Royal Ave E, Montreal, QC H2T 1N9",
        #    "1735 Rue Saint-Denis, Montréal, QC H2X 3K4",
        #    "2153 Mackay St, Montreal, QC H3G 2J2",
        #    "3515 Avenue Lacombe, Montréal, QC H3T 1M2",
        #    "5265 Queen Mary Rd, Montreal, QC H3W 1Y3"
        # ]