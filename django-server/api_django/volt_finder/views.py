from rest_framework import permissions, status, views, viewsets
from rest_framework.response import Response

from volt_finder.serializers import GeoCStationSerializer
from volt_finder import helpers_finder as hf

from main.serializers import ChargingStationSerializer
from main.models import ChargingStation
from volt_finder import mygooglemaps as gg

from django.utils import timezone 
import datetime as dt  
from volt_reservation.models import CSEvent


class ChargingStationTopNearListView(viewsets.ReadOnlyModelViewSet):
    """ Get's user POI and returns a short list of CS that are nearest to it
    :param poi_location: the point of interestan address
    :type destinations: a single location, as a string
    """
    permission_classes = (permissions.IsAuthenticated,)
    #TODO: apply some filtering to query (or ger_queryset()) to limit number of CS passed to google
    queryset = ChargingStation.objects.all()
    
    def get_top_cs_near_poi_no_date(self, request, poi_location):
        # Get All charging stations and pass their locations to getNearest       

        all_cs = self.queryset

        cs_addresses = [cs_inst.address for cs_inst in all_cs]
        
        gg_top_cs = gg.getNearestCS(poi_location, cs_addresses)        
        hf.match_cs_nk_based_on_address(gg_top_cs, all_cs)

        serializer = GeoCStationSerializer(gg_top_cs, many=True)

        return Response(serializer.data)

    def get_top_cs_near_poi_available_date(self, request, poi_location, date_x):    
        today = timezone.now().date()        

        events_cs = CSEvent.objects.filter(
                    status='AVAILABLE',
                    startDateTime__range=(today, today + dt.timedelta(days=1)))

        all_cs = [event.cs for event in events_cs]

        cs_addresses = [cs_inst.address for cs_inst in all_cs]
        
        gg_top_cs = gg.getNearestCS(poi_location, cs_addresses)        
        hf.match_cs_nk_based_on_address(gg_top_cs, all_cs)

        serializer = GeoCStationSerializer(gg_top_cs, many=True)

        return Response(serializer.data)

