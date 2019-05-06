from rest_framework import permissions, status, views, viewsets
from rest_framework.response import Response
from django.contrib.gis.geos import GEOSGeometry, fromstr
from django.contrib.gis.measure import D 
from django.contrib.gis.db.models.functions import Distance 

from volt_finder.serializers import GeoCStationSerializer
from volt_finder import helpers_finder as hf
from volt_reservation.models import EventCS
from volt_finder import mygooglemaps as gg

from main.serializers import ChargingStationSerializer
from main.models import ChargingStation

from volt_reservation.services import ReservationService

import datetime as dt  
from decimal import Decimal



class ChargingStationTopNearListView(viewsets.ReadOnlyModelViewSet):
    """ Get's user POI and returns a short list of CS that are nearest to it
    :param poi_location: the point of interestan address
    :type destinations: a single location, as a string
    """
    # permission_classes = (permissions.IsAuthenticated,)

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
                #TODO Get coordinates from user provided address (using google.api)
                poi_lat = Decimal(data.get('poi_lat'))
                poi_lng = Decimal(data.get('poi_lng'))
                poi_coords = fromstr(f'POINT({poi_lng} {poi_lat})', srid=4326)

                #TODO figure how to define max_dist in metters as opposed to degrees
                max_dist = 0.05  # about 3km
                #max_dist = D(m=3000)
                
                # Get all CS within max_dist (in meters) of POI, and annotate distance to poi               
                cs_near_poi = ChargingStation.objects.filter(
                    geo_location__dwithin=(poi_coords, max_dist)).annotate(
                        distance_to_poi = Distance("geo_location", poi_coords)
                        ).order_by("distance_to_poi")

                if len(cs_near_poi) > 10:
                    serializer = ChargingStationSerializer(cs_near_poi[0:10], many=True)
                    return Response(serializer.data)
                else:
                    serializer = ChargingStationSerializer(cs_near_poi, many=True)
                    return Response(serializer.data)
                
            return Response(serializer.data)
        else:
            return Response(None, status.HTTP_422_UNPROCESSABLE_ENTITY)