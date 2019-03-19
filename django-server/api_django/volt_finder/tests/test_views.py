from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from volt_finder.serializers import GeoCStationSerializer
from main.models import ChargingStation

PASSWORD = 'pAssw0rd!'
poi_location = '1101 Rue Rachel E Montreal, QC H2J 2J7' 

""" HELPER FUNC """
def create_user(username='user@example.com', password=PASSWORD):
    return get_user_model().objects.create_user(
        username=username, password=password)


""" TESTS """
class AuthenticationTest(APITestCase):
    #TODO test user.group==host can't use any finder endpoints
    def setUp(self):
        self.client = APIClient()
    
    @classmethod
    def setUpTestData(cls):
        cls.cs_t1 = ChargingStation.objects.create( 
            name     = 'Panthere 1',
            address  = '1251 Rue Jeanne-Mance, Montréal, QC H2X, Canada', 
            lat      = 45.5070394,
            lng      = -73.5651293
        )

    def test_annon_user_can_not_access_finder_cs_near_poi_endpoint(self):
        """ Attempt to access endpoints that require login as annon user (no-login) """
        response = self.client.get(
            reverse('volt_finder:cs_near_poi', kwargs={'poi_location': poi_location}))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)


class VoltFinderViewTest(APITestCase):
    """ Tests the ability to get the (single) nearest CS to user provided POI""" 
    #TODO Include def setUpTestData(cls): Class method to set up test data
    #TODO: move all CS created into this method
    # Check this: https://docs.djangoproject.com/en/2.1/topics/testing/tools/#django.test.TestCase

    def setUp(self):
        user = create_user()
        self.client = APIClient()
        self.client.login(username=user.username, password=PASSWORD)        

    
    def test_get_top_5_cs_near_poi(self):
        test_top_cs = [
            ChargingStation.objects.create(
                address='1735 Rue Saint-Denis, Montréal, QC H2X 3K4, Canada', name='Top 2'),
            ChargingStation.objects.create(
                address='1999 Avenue du Mont-Royal E, Montréal, QC H2H 1J4, Canada', name='Top 3'),
            ChargingStation.objects.create(
                address='145 Avenue du Mont-Royal E, Montréal, QC H2T 1N9, Canada', name='Top 4'),
            ChargingStation.objects.create(
                address='5333 Avenue de Gaspé #307, Montréal, QC H2T, Canada', name='Top 5'),
            ChargingStation.objects.create(
                address='160 Rue Saint Viateur E, Montréal, QC H2T 1A8, Canada', name='Top 1'),
        ]
        # CS farther from poi than test_top_cs
        other_cs = [ 
            ChargingStation.objects.create(
                address='545 Rue Milton, Montreal, QC H2X 1W5, Canada', name='test_1' ),
            ChargingStation.objects.create(
                address='2153 Rue Mackay, Montreal, QC H3G 2J2, Canada', name='test_2' ),
            ChargingStation.objects.create(
                address='191 Place du Marché-du-Nord, Montreal, QC H2S 1A2, Canada', name='test_3' ),
            ChargingStation.objects.create(
                address='3515 Avenue Lacombe, Montreal, QC H3T 1M2, Canada', name='test_4' ),
            ChargingStation.objects.create(
                address='5265 Chemin Queen Mary, Montreal, QC H3W 1Y3, Canada', name='test_5' )
        ]

        response = self.client.get(reverse('volt_finder:cs_near_poi', kwargs={'poi_location': poi_location}))
        serializer = GeoCStationSerializer(data=response.data,  many=True)  

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertTrue(serializer.is_valid())
        serialized_data = serializer.validated_data
        
        exp_cStation_nks = [cs.nk for cs in test_top_cs]
        other_cStation_nks = [cs.nk for cs in other_cs]
        act_cStation_nks = [cs['nk'] for cs in serialized_data]
        self.assertCountEqual(exp_cStation_nks, act_cStation_nks)
        self.assertAlmostEqual(act_cStation_nks, exp_cStation_nks)
        self.assertNotIn(other_cStation_nks[0], exp_cStation_nks)
        self.assertGreater(serialized_data[1]['duration_val'], serialized_data[0]['duration_val'])
