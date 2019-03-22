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

    def setUp(self):
        user = create_user()
        self.client = APIClient()
        self.client.login(username=user.username, password=PASSWORD)        

    @classmethod
    def setUpTestData(cls):
        cls.test_top_cs = [
            ChargingStation.objects.create( 
                name     = 'CS_t_top_1',
                address  = '4365 Rue Cartier, Montréal, QC H2H 2N9, Canada', 
                lat      = 45.533234,
                lng      = -73.571813),   
            ChargingStation.objects.create( 
                name     = 'CS_t_top_2',
                address  = '1956 Rue Frontenac, Montréal, QC H2K 2Z1, Canada', 
                lat      = 45.5325695,
                lng      = -73.5521119), 
            ChargingStation.objects.create( 
                name     = 'CS_t_top_3',
                address  = '1251 Rue Jeanne-Mance, Montréal, QC H2X, Canada', 
                lat      = 45.5070394,
                lng      = -73.5651293), 
            ChargingStation.objects.create( 
                name     = 'CS_t_top_4',
                address  = '6679 Rue Garnier, Montréal, QC H2G 3A2, Canada', 
                lat      = 45.542892,
                lng      = -73.60115),    
            ChargingStation.objects.create( 
                name     = 'CS_t_top_5',
                address  = '6511 Rue Saint-André, Montréal, QC H2S 2K7, Canada', 
                lat      = 45.536734,
                lng      = -73.6030444),         
        ]
        cls.test_other_cs = [ 
            ChargingStation.objects.create( 
                name     = 'CS_t_oth_1',
                address  = '205 Rue Chabanel O, Montréal, QC H2N 1G3, Canada', 
                lat      = 45.540977,
                lng      = -73.6536969),
            ChargingStation.objects.create( 
                name     = 'CS_t_oth_2',
                address  = '10625 Rue Francis, Montréal, QC H2C 3A5, Canada', 
                lat      = 45.5653481,
                lng      = -73.6603467),       
            ChargingStation.objects.create( 
                name     = 'CS_t_oth_3',
                address  = '1530 Rue Fleury E, Montréal, QC H2C 2Y6, Canada', 
                lat      = 45.5629748,
                lng      = -73.6561512),    
            ]
                
    
    def test_get_top_5_cs_near_poi(self):
        response = self.client.get(reverse(
                    'volt_finder:cs_near_poi', kwargs={'poi_location': poi_location}))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        serializer = GeoCStationSerializer(data=response.data,  many=True)  

        self.assertTrue(serializer.is_valid())
        serialized_data = serializer.validated_data
        
        exp_cStation_nks = [cs.nk for cs in self.test_top_cs]
        other_cStation_nks = [cs.nk for cs in self.test_other_cs]
        act_cStation_nks = [cs['nk'] for cs in serialized_data]

        self.assertCountEqual(exp_cStation_nks, act_cStation_nks)
        self.assertAlmostEqual(act_cStation_nks, exp_cStation_nks)
        self.assertNotIn(other_cStation_nks[0], exp_cStation_nks)
        self.assertGreater(serialized_data[1]['duration_val'], serialized_data[0]['duration_val'])
