from rest_framework import permissions, status, views, viewsets
from rest_framework.response import Response

from volt_finder.serializers import GeoCStationSerializer
from main.serializers import ChargingStationSerializer
from main.models import ChargingStation
from . import mygooglemaps as gg


class ChargingStationTopNearListView(viewsets.ReadOnlyModelViewSet):
    """ Get's user POI and returns a short list of CS that are nearest to it
    :param poi_location: the point of interestan address
    :type destinations: a single location, as a string
    """
    permission_classes = (permissions.IsAuthenticated,)
    #TODO: apply some filtering to query (or ger_queryset()) to limit number of CS passed to google
    queryset = ChargingStation.objects.all()
    
    def top_cs_near_poi(self, request, poi_location):
        # Get All charging stations and pass their locations to getNearest       

        all_cs = self.queryset

        cs_addresses = [i.address for i in all_cs]
        top_cs = gg.getNearestCS(poi_location, cs_addresses)

        # Match CS info from queryset to top_cs, based on address
        # TODO conver this for loop into a helper function and move it to that file
        for cs in top_cs:
            xnk = next((x for x in all_cs if x.address == cs.destination_addresses), None)
            if xnk != None:
                cs.nk = str(xnk)
            else:
                pass
            #TODO: USE try and except
            #TODO: add other relevant CS fields (update CS data class in gg module)
           
        serializer = GeoCStationSerializer(top_cs, many=True)

        return Response(serializer.data)

        

