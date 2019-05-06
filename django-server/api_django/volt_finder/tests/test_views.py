from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from volt_finder.serializers import GeoCStationSerializer
from main.models import ChargingStation
from main.serializers import ChargingStationSerializer
from volt_reservation.models import EventEV, EventCS

from django.utils import timezone 
import datetime as dt  



PASSWORD = 'pAssw0rd!'
# POI_LOCATION = '1101 Rue Rachel E Montreal, QC H2J 2J7' 
POI_LOCATION = {"lat": 45.5260525, "lng": -73.5596788}
POI_LAT, POI_LNG = 45.5260525, -73.5596788

today = timezone.now().date()
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
        host = create_user()
        cls.cs_t1 = ChargingStation.objects.create( 
            name     = 'Panthere 1',
            address  = '1251 Rue Jeanne-Mance, Montréal, QC H2X, Canada', 
            lat      = 45.5070394,
            lng      = -73.5651293,
            cs_host  = host
        )

    # def test_annon_user_can_not_access_finder_cs_near_poi_endpoint(self):
    #     """ Attempt to access endpoints that require login as annon user (no-login) """
    #     response = self.client.get(reverse('volt_finder:near-poi-list'),
    #                                data={'poi_location': poi_location})#, 'date_x':today}))
    #     self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)


class VoltFinderViewTest(APITestCase):
    """ Tests the ability to get the (single) nearest CS to user provided POI""" 

    def setUp(self):
        user = create_user()
        self.client = APIClient()
        self.client.login(username=user.username, password=PASSWORD)        

    @classmethod
    def setUpTestData(cls):
        host = create_user(username='host')
        cls.test_top_cs = [
            ChargingStation.objects.create(
                name ="636 | BSR | VM | 2005 Ste-Catherine E", external_id = "CEA-11298", 
                charge_level = "Level2", tarif_text = "1,00 $ (CAD)  par heure", 
                address = "2005 Rue Sainte-Catherine E, Montréal, QC H2K 2H6, Canada", 
                city = "Montréal", province = "QCCanada", postal_code = "H2K 2H6", 
                lat = 45.5244401, lng = -73.5510127, cs_host = host),
            ChargingStation.objects.create( 
                name     = 'CS_t_top_2',
                address  = '1956 Rue Frontenac, Montréal, QC H2K 2Z1, Canada', 
                lat      = 45.5325695,
                lng      = -73.5521119,
                cs_host  = host),
            ChargingStation.objects.create( 
                name     = 'CS_t_top_1',
                address  = '4365 Rue Cartier, Montréal, QC H2H 2N9, Canada', 
                lat      = 45.533234,
                lng      = -73.571813,
                cs_host  = host),   
            ChargingStation.objects.create(
                name ="501 | BSR | PMR | 4492 rue Parth", external_id = "CEA-10372", 
                charge_level = "Level2", tarif_text = "1,00 $ (CAD)  par heure", 
                address = "4492 Rue Parthenais, Montréal, QC H2H 2G5, Canada", 
                city = "Montréal", province = "QCCanada", postal_code = "H2H 2G5", 
                lat = 45.536284, lng = -73.5709799, cs_host = host), 
            ChargingStation.objects.create(
                name ="626 | BSR | VM | 2027 L'Espérance", external_id = "CEA-10174",
                charge_level = "Level2", tarif_text = "1,00 $ (CAD)  par heure", 
                address = "2030 Rue Lespérance, Montréal, QC H2K 2N9, Canada", 
                city = "Montréal", province = "QCCanada", postal_code = "H2K 2N9", 
                lat = 45.537695, lng = -73.550104, cs_host = host),
            ChargingStation.objects.create(
                name ="SHDM - Complexe Chaussegros-De-Léry", external_id = "CEA-386", 
                charge_level = "Level2", tarif_text = "2,50 $ (CAD)  par session", 
                address = "330 Rue du Champ de Mars, Montréal, QC H2Y 3Z8, Canada", 
                city = "Montréal", province = "QCCanada", postal_code = "H2Y 3Z3", 
                lat = 45.5100013, lng = -73.5536221, cs_host = host),
            ChargingStation.objects.create(
                name ="512 | BSR | PMR | 1 Mont-Royal Est", external_id = "CEA-10561",
                 charge_level = "Level2", tarif_text = "1,00 $ (CAD)  par heure", 
                 address = "1 Avenue du Mont-Royal E, Montréal, QC H2T 1N4, Canada", 
                 city = "Montréal", province = "QCCanada", postal_code = "H2T 1N4", 
                 lat = 45.520303, lng = -73.586452, cs_host = host),
            ChargingStation.objects.create(
                name ="514 | BSR | PMR | 5333 Papineau", external_id = "CEA-10522", 
                charge_level = "Level2", tarif_text = "1,00 $ (CAD)  par heure", 
                address = "5333 Rue Papineau, Montréal, QC H2H 1W1, Canada", 
                city = "Montréal", province = "QCCanada", postal_code = "H2H 1W1", 
                lat = 45.5369802, lng = -73.5830187, cs_host = host),
            ChargingStation.objects.create(name ="581 | BHR | PMR | 5633 Saint-Dominique : Aréna St-Louis", external_id = "CEA-111", charge_level = "Level2", tarif_text = "2,50 $ (CAD)  par session", address = "5633 Rue Saint-Dominique, Montréal, QC H2T 1V7, Canada", city = "Montréal", province = "QC", country = "Canada", postal_code = "H2T 1V7", lat = 45.5273112, lng = -73.5994845, cs_host = host),
            ChargingStation.objects.create(name ="328 | BSR | RPP | 440 Beaubien", external_id = "CEA-11467", charge_level = "Level2", tarif_text = "1,00 $ (CAD)  par heure", address = "440 Rue Beaubien E, Montréal, QC H2S 1S3, Canada", city = "Montréal", province = "QCCanada", postal_code = "H2S 2P7", lat = 45.534534, lng = -73.604271, cs_host = host), 
        ]
        cls.test_other_cs = [ 
            ChargingStation.objects.create( 
                name     = 'CS_t_oth_1',
                address  = '205 Rue Chabanel O, Montréal, QC H2N 1G3, Canada', 
                lat      = 45.540977,
                lng      = -73.6536969,
                cs_host  = host),
            ChargingStation.objects.create( 
                name     = 'CS_t_oth_2',
                address  = '10625 Rue Francis, Montréal, QC H2C 3A5, Canada', 
                lat      = 45.5653481,
                lng      = -73.6603467,
                cs_host  = host),       
            ChargingStation.objects.create( 
                name     = 'CS_t_oth_3',
                address  = '1530 Rue Fleury E, Montréal, QC H2C 2Y6, Canada', 
                lat      = 45.5629748,
                lng      = -73.6561512,
                cs_host  = host),  
            ChargingStation.objects.create( 
                name     = 'CS_t_top_4',
                address  = '6679 Rue Garnier, Montréal, QC H2G 3A2, Canada', 
                lat      = 45.542892,
                lng      = -73.60115,
                cs_host  = host),      
            ChargingStation.objects.create(name ="220 | BSR | VSMPE | 7151 St-Dominique", external_id = "CEA-10599", charge_level = "Level2", tarif_text = "1,00 $ (CAD)  par heure", address = "7151 Rue Saint-Dominique, Montréal, QC H2R 1X3, Canada", city = "Montréal", province = "QCCanada", postal_code = "H2R 1X3", lat = 45.535179, lng = -73.6173677, cs_host = host),
            ChargingStation.objects.create(name ="214 | BSR | VSMPE | 6961 des Écores", external_id = "CEA-10693", charge_level = "Level2", tarif_text = "1,00 $ (CAD)  par heure", address = "6961 Rue des Écores, Montréal, QC H2E 2V7, Canada", city = "Montréal", province = "QCCanada", postal_code = "H2E 2V7", lat = 45.5511632, lng = -73.5999005, cs_host = host),
            ChargingStation.objects.create(name ="208 | BSR | VSMPE | 10 Villeray", external_id = "CEA-10365", charge_level = "Level2", tarif_text = "1,00 $ (CAD)  par heure", address = "10 Rue Villeray, Montréal, QC H2R 1E8, Canada", city = "Montréal", province = "QCCanada", postal_code = "H2R 1E8", lat = 45.537246, lng = -73.624707, cs_host = host),
            ChargingStation.objects.create(name ="219 | BSR | VSMPE | 1210 Villeray", external_id = "CEA-10703", charge_level = "Level2", tarif_text = "1,00 $ (CAD)  par heure", address = "1210 Rue Villeray, Montréal, QC H2R 1J7, Canada", city = "Montréal", province = "QCCanada", postal_code = "H2R 1J7", lat = 45.5468335, lng = -73.6184014, cs_host = host),
            ChargingStation.objects.create(name ="326 | BSR | RPP | 1550 Bélanger", external_id = "CEA-11218", charge_level = "Level2", tarif_text = "1,00 $ (CAD)  par heure", address = "1550 Rue Bélanger, Montréal, QC H2G 1A9, Canada", city = "Montréal", province = "QCCanada", postal_code = "H2G 1A8", lat = 45.5453854, lng = -73.6040377, cs_host = host),  
            
            ]
        
        # cs_t1, cs_t2 = cls.test_top_cs[0], cls.test_top_cs[1]
        # cs_o1, cs_o2 = cls.test_other_cs[0], cls.test_other_cs[1]

        # t_start = timezone.now()
        # t_end   = t_start + dt.timedelta(minutes=30) 
        
        # event_1 = EventCS.objects.create( 
        #             startDateTime = t_start,
        #             endDateTime   = t_end,
        #             cs            = cs_t1
        #         )
        # event_2 = EventCS.objects.create( 
        #             startDateTime = t_start,
        #             endDateTime   = t_end,
        #             cs            = cs_o1
        #         )

    def test_get_top_10_cs_near_poi_status_any(self):
        response = self.client.get(reverse('volt_finder:near-poi-list'),
                                   data={'poi_location': POI_LOCATION,
                                         'poi_lat': POI_LAT,
                                         'poi_lng': POI_LNG})

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        
        #TODO Use serializer to validate response.data (and use validate_data instead)
        # serializer = ChargingStationSerializer(data=response.data,  many=True) 
        # self.assertTrue(serializer.is_valid())
        # serialized_data = serializer.validated_data 
        # print("# serializer data: ", serializer )
        # print("# serializer is valid: ", serializer.is_valid())
        # print("# validation error: ", serializer.errors)
        # print("# VALIDATED serializer data: ", serializer.validated_data )
        # print("# 1st ITEM: ", serializer.validated_data[0].items())
        # print("# 1st ITEM stuff: ", serializer.validated_data[0].items())
        
        
        rdata = response.data
        # print("# Response data: ", rdata )
        exp_cs_nks   = [cs.nk for cs in self.test_top_cs]
        other_cs_nks = [cs.nk for cs in self.test_other_cs]
        
        all_cs = ChargingStation.objects.all()
        print("# ALL CS: ", len(all_cs))
        print("# OThER CS: ", len(self.test_other_cs))
        print("# TOP CS: ", len(self.test_top_cs))

        for cs in other_cs_nks: print(cs)
            #f"{cs.id} / {cs.distance_to_poi} / {cs.address}")

        act_cs_nks   = [cs.get('nk') for cs in rdata]
        print("# ID + Distance: ")
        for cs in rdata: print(f"{cs.get('id')} / {cs.get('distance_to_poi')} / {cs.get('address')}")
        # self.assertCountEqual(expected_cs_nk, response_cs_nks)
        # self.assertAlmostEqual(response_cs_nks, expected_cs_nk)
        self.assertNotIn(other_cs_nks[0], act_cs_nks)

        self.assertEqual(10, len(rdata))
        self.assertGreaterEqual(rdata[1].get('distance_to_poi'), rdata[0]['distance_to_poi'])
        self.assertGreaterEqual(rdata[2].get('distance_to_poi'), rdata[1]['distance_to_poi'])
        self.assertGreater(rdata[3].get('distance_to_poi'), rdata[0]['distance_to_poi'])



    # def test_get_top_10_cs_near_poi_status_any(self):
    #     response = self.client.get(reverse('volt_finder:near-poi-list'),
    #                                data={'poi_location': POI_LOCATION})

    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     serializer = GeoCStationSerializer(data=response.data,  many=True)  

    #     self.assertTrue(serializer.is_valid())
    #     serialized_data = serializer.validated_data
        
    #     exp_cStation_nks   = [cs.nk for cs in self.test_top_cs]
    #     other_cStation_nks = [cs.nk for cs in self.test_other_cs]
    #     act_cStation_nks   = [cs['nk'] for cs in serialized_data]

    #     self.assertCountEqual(exp_cStation_nks, act_cStation_nks)
    #     self.assertAlmostEqual(act_cStation_nks, exp_cStation_nks)
    #     self.assertNotIn(other_cStation_nks[0], exp_cStation_nks)
    #     self.assertGreater(serialized_data[1]['duration_val'], serialized_data[0]['duration_val'])


    # def test_get_top_cs_near_poi_status_available_today(self):
    #     start_datetime = timezone.now().date()
    #     end_datetime = start_datetime + dt.timedelta(days=1)
    #     response = self.client.get(reverse('volt_finder:near-poi-list'),
    #                                data={'poi_location': POI_LOCATION,
    #                                      'start_datetime': start_datetime,
    #                                      'end_datetime': end_datetime})

    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     serializer = GeoCStationSerializer(data=response.data,  many=True)  

    #     self.assertTrue(serializer.is_valid())
    #     serialized_data = serializer.validated_data
    #     exp_cs_nks = [self.test_top_cs[0].nk, self.test_other_cs[0].nk]
    #     act_cs_nks = [cs['nk'] for cs in serialized_data]


    def test_resp_422_to_incomplete_request(self):
        response = self.client.get(reverse('volt_finder:near-poi-list'))

        self.assertEqual(status.HTTP_422_UNPROCESSABLE_ENTITY, response.status_code)