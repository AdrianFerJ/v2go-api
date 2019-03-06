from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.forms import AuthenticationForm 

from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

import json

from .serializers import UserSerializer, ChargingStationSerializer, GeoCStationSerializer
from .models import ChargingStation
from . import mygooglemaps as gg


class SignUpView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class LogInView(views.APIView):
    def post(self, request):
        form = AuthenticationForm(data=request.data)
        if form.is_valid():
            user = form.get_user()
            login(request, user=form.get_user())
            return Response(UserSerializer(user).data)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class LogOutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, *args, **kwargs):
        logout(self.request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChargingStationListView(viewsets.ReadOnlyModelViewSet):
    """ Basic CharginStation view, returns a list of CS near user """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = ChargingStation.objects.all()
    serializer_class = ChargingStationSerializer


class ChargingStationDetailView(viewsets.ReadOnlyModelViewSet):  
    """ Get's a32char nk and returns CS's detail info that matches the nk """
    lookup_field = 'nk'
    lookup_url_kwarg = 'cStation_nk'
    permission_classes = (permissions.IsAuthenticated,)
    queryset = ChargingStation.objects.all()
    serializer_class = ChargingStationSerializer


class ChargingStationTopNearListView(viewsets.ReadOnlyModelViewSet):
    """ Get's user POI and returns a short list of CS that are nearest to it
    :param poi_location: the point of interestan address
    :type destinations: a single location, as a string
    """
    permission_classes = (permissions.IsAuthenticated,)
    #TODO: replace queryset by a get_queryset() method and apply some filtering to either the query or the output
    queryset = ChargingStation.objects.all()
    
    def top_cs_near_poi(self, request, poi_location):
        # Get All charging stations and pass their locations to getNearest       

        all_cs = self.queryset

        cs_loc = [i.location for i in all_cs]
        top_cs = gg.getNearestCS(poi_location, cs_loc)

        # Match CS info from queryset to top_cs, based on address
        for cs in top_cs:
            xnk = next((x for x in all_cs if x.location == cs.destination_addresses), None)
            if xnk != None:
                cs.nk = str(xnk)
            else:
                pass
            #TODO: USE try and except
            #TODO: add other relevant CS fields (update CS data class in gg module)
           
        serializer = GeoCStationSerializer(top_cs, many=True)

        return Response(serializer.data)

        

