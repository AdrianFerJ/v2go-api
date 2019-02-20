from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.forms import AuthenticationForm 

from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.response import Response

from .serializers import UserSerializer, ChargingStationSerializer
from volt_finder.models import ChargingStation

from volt_finder import mygooglemaps as gg


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
    """ Get's user POI and returns a short list of CS that are nearest to it """
    #poi_location = 'poi_location'
    permission_classes = (permissions.IsAuthenticated,)
    # serializer_class = ChargingStationSerializer
    
    def top_cs_near_poi(self, request, poi_location):
        queryset = ChargingStation.objects.all()
        
        #TODO: call distance matrix
        cs_loc = [i.location for i in queryset]
        top_cs = gg.getNearestCS(poi_location, cs_loc)
        return Response(top_cs)


        #TODO: select top results
        #TODO: return serialized (TOP) CS
        # serializer = ChargingStationSerializer(queryset, many=True)
        # return Response(serializer.data)
        



#   if len(results) > 5:
#         top_marks = results[:5]
#     else:
#         top_marks = results