from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from main.serializers import ChargingStationSerializer #, UserSerializer, GeoCStationSerializer
from main.models import ChargingStation


""" HELPER FUNC """
PASSWORD = 'pAssw0rd?XD'
USERNAME = 'user@example.com'
U_DRIVER = 'DRIVER'
U_OWNER  = 'OWNER'

def create_user(username=USERNAME, password=PASSWORD, group=U_DRIVER):
    return get_user_model().objects.create_user(
        username=username, password=password)
        #TODO add group=group


""" TESTS """
class AuthenticationTest(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_user_can_sign_up(self):
        # photo_file = create_photo_file() #TODO: enable user photo
        response = self.client.post(reverse('sign_up'), data={
            'username': USERNAME,
            'first_name': 'Test_name',
            'last_name': 'Test_last',
            'password1': PASSWORD,
            'password2': PASSWORD,
            'group': 'driver',
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


class HostChargingStationTest(APITestCase):
    """ Test all Model-backed API views for CS (only available for cs Owner
        #TODO setUp() should create user with group=U_OWNER)
    """
    def setUp(self):
        user = create_user() #group=U_OWNER)
        self.client = APIClient()
        self.client.login(username=user.username, password=PASSWORD)   
    
    @classmethod
    def setUpTestData(cls):
        cls.cs_t1 = ChargingStation.objects.create( 
            name     = 'Panthere 1',
            address  = '1251 Rue Jeanne-Mance, Montréal, QC H2X, Canada', 
            lat      = 45.5070394,
            lng      = 45.5070394
        )
        cls.cs_t2 = ChargingStation.objects.create( 
            name     = 'Panthere 2',
            address  = '1251 Rue Jeanne-Mance, Montréal, QC H2X, Canada', 
            lat      = 45.5070394,
            lng      = 45.5070394
        )
    
    def host_can_retrieve_cs_detail_test(self):
        # cStation = ChargingStation.objects.create(
        #     address='160 Rue Saint Viateur E, Montreal, QC H2T 1A8', name='Panthere 1')
        print("# self.cs_t1.get_absolute_url()", self.cs_t1.get_absolute_url())
        response = self.client.get(self.cs_t1.get_absolute_url())
        print("# response.data.get('nk')", response.data.get('nk'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.cs_t1.nk, response.data.get('nk'))
    
    def host_can_retrive_cs_list_test(self):
        """ Get CS list
            #TODO: should display only CS created by group=U_OWNER)
        """
        response = self.client.get(reverse('main:host_cs_list'))

        exp_cs_nks = [self.cs_t1.nk, self.cs_t2.nk]
        act_cs_nks = [cs.get('nk') for cs in response.data]

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertCountEqual(exp_cs_nks, act_cs_nks)
    


    # def test_host_can_create_cs(self):
	# 	"""CS creation"""