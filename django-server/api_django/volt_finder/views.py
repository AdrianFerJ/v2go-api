from rest_framework import permissions, status, views, viewsets
from rest_framework.response import Response

from volt_finder.serializers import GeoCStationSerializer
from volt_finder import helpers_finder as hf

from main.serializers import ChargingStationSerializer
from main.models import ChargingStation
from volt_finder import mygooglemaps as gg
from volt_reservation.services import ReservationService

import datetime as dt  
from volt_reservation.models import EventCS


class ChargingStationTopNearListView(viewsets.ReadOnlyModelViewSet):
    """ Get's user POI and returns a short list of CS that are nearest to it
    :param poi_location: the point of interestan address
    :type destinations: a single location, as a string
    """
    permission_classes = (permissions.IsAuthenticated,)
    #TODO: apply some filtering to query (or ger_queryset()) to limit number of CS passed to google
    queryset = ChargingStation.objects.all()

    def list(self, request, *args, **kwargs):
        data = request.GET

        if 'poi_location' in data:
            if 'start_datetime' in data and 'end_datetime' in data:
                start_datetime = data.get('start_datetime')
                end_datetime = data.get('end_datetime')

                events_cs = ReservationService.get_available_event_cs(start_datetime, end_datetime)

                all_cs = [event.cs for event in events_cs]

                cs_addresses = [cs_inst.address for cs_inst in all_cs]
                
                gg_top_cs = gg.getNearestCS(data.get('poi_location'), cs_addresses)        
                hf.match_cs_nk_based_on_address(gg_top_cs, all_cs)

                serializer = GeoCStationSerializer(gg_top_cs, many=True)
            else:
                all_cs = self.queryset

                cs_addresses = [cs_inst.address for cs_inst in all_cs]
                
                gg_top_cs = gg.getNearestCS(data.get('poi_location'), cs_addresses)        
                hf.match_cs_nk_based_on_address(gg_top_cs, all_cs)

                serializer = GeoCStationSerializer(gg_top_cs, many=True)

            return Response(serializer.data)
        else:
            return Response(None, status.HTTP_422_UNPROCESSABLE_ENTITY)