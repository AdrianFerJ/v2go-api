from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from volt_finder.serializers import ChargingStationSerializer, UserSerializer
from volt_finder.models import ChargingStation

PASSWORD = 'pAssw0rd!'

""" HELPER FUNC """
def create_user(username='user@example.com', password=PASSWORD):
    return get_user_model().objects.create_user(
        username=username, password=password)

sample_addrs = [
    "160 Rue Saint Viateur E, Montreal, QC H2T 1A8",
    "145 Mont-Royal Ave E, Montreal, QC H2T 1N9",
    "1735 Rue Saint-Denis, Montreal, QC H2X 3K4",
    "2153 Mackay St, Montreal, QC H3G 2J2",
    "3515 Avenue Lacombe, Montreal, QC H3T 1M2",
    "5265 Queen Mary Rd, Montreal, QC H3W 1Y3",
    "191 Place du Marché-du-Nord, Montreal, QC H2S 1A2",
    "545 Milton St, Montreal, QC H2X 1W5",
    "1999 Mont-Royal Ave E, Montreal, QC H2H 1J4",
    "432 Rue Rachel E, Montreal, QC H2J 2G7"
]


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

    def test_user_can_retrieve_cs_detail_by_nk(self):
        cStation = ChargingStation.objects.create(
            location='160 Rue Saint Viateur E, Montreal, QC H2T 1A8', name='Panthere 1', manager_id=1)
        response = self.client.get(cStation.get_absolute_url())
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(cStation.nk, response.data.get('nk'))
    
    def test_get_list_of_cs_no_params(self):  
        cStations = [
            ChargingStation.objects.create(
                location='432 Rue Rachel E, Montreal, QC H2J 2G7, Canada', name='Panthere 1', manager_id=1),
            ChargingStation.objects.create(
                location='1735 Rue Saint-Denis, Montreal, QC H2X 3K4, Canada', name='Panthere 2', manager_id=1),
            ChargingStation.objects.create(
                location='2153 Mackay St, Montreal, QC H3G 2J2', name='Panthere 3', manager_id=1),
        ]      
        response = self.client.get(reverse('cStation:cStations_list'))

        print('********** RESPONSE DATA  P1: #', len(response.data), 'TYPE:', type(response.data), '**********')
        print(response.data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        exp_cStation_nks = [cs.nk for cs in cStations]
        act_cStation_nks = [cs.get('nk') for cs in response.data]
        self.assertCountEqual(exp_cStation_nks, act_cStation_nks)
    
    def test_get_top_5_cs_near_poi(self):
        #TODO: Fix / add
        #       - use len(ExpectedcStations) == len(APIoutPutcStations)
        #       - and self.assertCountEqual(exp_cStation_nks, act_cStation_nks)
        #       - *ExpectedcStations == ChargingStation.objects.all()
        poi_location = '1101 Rue Rachel E Montreal, QC H2J 2J7' 
        test_top_cs = [
            ChargingStation.objects.create(
                location='1735 Rue Saint-Denis, Montréal, QC H2X 3K4, Canada', name='Top 2', manager_id=1),
            ChargingStation.objects.create(
                location='1999 Avenue du Mont-Royal E, Montréal, QC H2H 1J4, Canada', name='Top 3', manager_id=1),
            ChargingStation.objects.create(
                location='145 Avenue du Mont-Royal E, Montréal, QC H2T 1N9, Canada', name='Top 4', manager_id=1),
            ChargingStation.objects.create(
                location='5333 Avenue de Gaspé #307, Montréal, QC H2T, Canada', name='Top 5', manager_id=1),
            ChargingStation.objects.create(
                location='160 Rue Saint Viateur E, Montréal, QC H2T 1A8, Canada', name='Top 1', manager_id=1),
        ]
        #other_cs (farther from poi)
        ChargingStation.objects.create(
            location='545 Rue Milton, Montreal, QC H2X 1W5, Canada', name='test_1', manager_id=1)
        ChargingStation.objects.create(
            location='2153 Rue Mackay, Montreal, QC H3G 2J2, Canada', name='test_2', manager_id=1)
        ChargingStation.objects.create(
            location='191 Place du Marché-du-Nord, Montreal, QC H2S 1A2, Canada', name='test_3', manager_id=1)
        ChargingStation.objects.create(
            location='3515 Avenue Lacombe, Montreal, QC H3T 1M2, Canada', name='test_4', manager_id=1)
        ChargingStation.objects.create(
            location='5265 Chemin Queen Mary, Montreal, QC H3W 1Y3, Canada', name='test_5', manager_id=1)
        
        # TODO: Fix reverse call to include poi_location in get.request
        # response = self.client.get(reverse('cStation:cStations_near_poi'))
        # response = self.client.get(reverse('cStation:cStations_near_poi', args=[poi_location]))
        response = self.client.get(reverse('cStation:cStations_near_poi', kwargs={'poi_location': poi_location}))
        
        #REMOVE
        print('#')
        print('********** RESPONSE DATA  P2: #', len(response.data), 'TYPE:', type(response.data), '**********')
        print(response.data)

        """ 
            RE-serialize data 
        """
        # import io
        # from rest_framework.parsers import JSONParser
        from volt_finder.serializers import GeoCStationSerializer
        # stream = io.BytesIO(response.data)
        # data = JSONParser().parse(stream)
        # serializer = GeoCStationSerializer(data=data,  many=True)

        serializer = GeoCStationSerializer(data=response.data,  many=True)       
        #TODO: replace if/else with TRY EXCEPT
        if serializer.is_valid():
            serializer.is_valid()
            serialized_data = serializer.validated_data
            print('#')
            print('~~~~~~~~ SERIALIZED DATA  !!!!: #', len(serialized_data), 'TYPE:', type(serialized_data), '**********')
        else:
            print('#')
            print('??????????? ERROR... XD  !!!!:')
            print(serializer.errors)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # EXP...
        exp_cStation_nks = [cs.nk for cs in test_top_cs]
        print('**********')  
        print('exp_cStation_nks = ', exp_cStation_nks)

        # act_cStation_nks = [cs.get('nk') for cs in response.data]  
        # act_cStation_nks = [cs.nk for cs in response.data]            
        # act_cStation_nks = [cs['nk'] for cs in response.data]
        act_cStation_nks = [cs['nk'] for cs in serialized_data]

        print('**********')  
        print('act_cStation_nks = ', act_cStation_nks)
        
        self.assertCountEqual(exp_cStation_nks, act_cStation_nks)
        # self.assertEqual(exp_cStation_nks[0], response.data)
        



    #TODO: def test_find_single_nearest_cs_to_poi(self):
    #   user_poi_location = '969 Rachel St E, Montreal, QC H2J 2J2'


      # panthereLocations = [,
        #    "145 Mont-Royal Ave E, Montreal, QC H2T 1N9",
        #    "1735 Rue Saint-Denis, Montreal, QC H2X 3K4",
        #    "2153 Mackay St, Montreal, QC H3G 2J2",
        #    "3515 Avenue Lacombe, Montreal, QC H3T 1M2",
        #    "5265 Queen Mary Rd, Montreal, QC H3W 1Y3"
        # ]

# def setUp():
#      client = APIClient()
#      client.login(username='test1', password='letmein!')
#      return client
