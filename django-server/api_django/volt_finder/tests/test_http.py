from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from volt_finder.serializers import ChargingStationSerializer, UserSerializer, GeoCStationSerializer
from volt_finder.models import ChargingStation

PASSWORD = 'pAssw0rd!'

""" HELPER FUNC """
def create_user(username='user@example.com', password=PASSWORD):
    return get_user_model().objects.create_user(
        username=username, password=password)


""" TESTS """
class AuthenticationTest(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_user_can_sign_up(self):
        # photo_file = create_photo_file() #TODO: enable user photo
        response = self.client.post(reverse('sign_up'), data={
            'username': 'user@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': PASSWORD,
            'password2': PASSWORD,
            'group': 'rider',
            # 'photo': photo_file,
        })
        user = get_user_model().objects.last()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.data['id'], user.id)
        self.assertEqual(response.data['username'], user.username)
        self.assertEqual(response.data['first_name'], user.first_name)
        self.assertEqual(response.data['last_name'], user.last_name)
        #self.assertEqual(response.data['group'], user.group) #TODO: enable user gorup (driver or cs_owner)
        #self.assertIsNotNone(user.photo) #TODO: enable user photo ID

    def test_user_can_log_in(self):
        user = create_user()
        response = self.client.post(reverse('log_in'), data={
            'username': user.username,
            'password': PASSWORD,
        })
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data['username'], user.username)

    def test_user_can_log_out(self):
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

    #TODO Include def setUpTestData(cls): Class method to set up test data
    #TODO: move all CS created into this method
    # Check this: https://docs.djangoproject.com/en/2.1/topics/testing/tools/#django.test.TestCase


    def test_user_can_retrieve_cs_detail_by_nk(self):
        cStation = ChargingStation.objects.create(
            address='160 Rue Saint Viateur E, Montreal, QC H2T 1A8', name='Panthere 1')
        response = self.client.get(cStation.get_absolute_url())
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(cStation.nk, response.data.get('nk'))
    
    def test_get_list_of_cs_no_params(self):  
        cStations = [
            ChargingStation.objects.create(
                address='432 Rue Rachel E, Montreal, QC H2J 2G7, Canada', name='Panthere 1'),
            ChargingStation.objects.create(
                address='1735 Rue Saint-Denis, Montreal, QC H2X 3K4, Canada', name='Panthere 2'),
            ChargingStation.objects.create(
                address='2153 Mackay St, Montreal, QC H3G 2J2, Canada', name='Panthere 3'),
        ]      
        response = self.client.get(reverse('cStation:cStations_list'))

        exp_cStation_nks = [cs.nk for cs in cStations]
        act_cStation_nks = [cs.get('nk') for cs in response.data]

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertCountEqual(exp_cStation_nks, act_cStation_nks)
    
    def test_get_top_5_cs_near_poi(self):
        poi_location = '1101 Rue Rachel E Montreal, QC H2J 2J7' 
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

        response = self.client.get(reverse('cStation:cStations_near_poi', kwargs={'poi_location': poi_location}))
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
        self.assertEqual(serialized_data[0]['duration_val'], 321)
        
