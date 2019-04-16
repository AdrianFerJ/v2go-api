from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.forms import AuthenticationForm 

from main.models import ChargingStation
from main.models import ElectricVehicle as EV
from main.serializers import ChargingStationSerializer, UserSerializer, EVSerializer
                             #CSHostSerializer, EVOwnerSerializer, EVSerializer#, GeoCStationSerializer
from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

""" 
    Views
"""
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


class ChargingStationList(generics.ListCreateAPIView):
    #TODO rename to ChargingStationCSCreateList
    #TODO host can only see her own CS, but no CSs owned by another host
    permission_classes = (permissions.IsAuthenticated,)
    queryset = ChargingStation.objects.all()
    serializer_class = ChargingStationSerializer


class ChargingStationDetail(generics.RetrieveUpdateDestroyAPIView):
    #TODO host can only see her own CS, but no CSs owned by another host
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'nk'
    lookup_url_kwarg = 'station_nk'
    queryset = ChargingStation.objects.all()
    serializer_class = ChargingStationSerializer


# class CSHostList(generics.ListCreateAPIView):
#     queryset = CSHost.objects.all()
#     serializer_class = CSHostSerializer


# class CSHostDetail(generics.RetrieveUpdateDestroyAPIView):
#     lookup_field = 'nk'
#     lookup_url_kwarg = 'cs_host_nk'
#     queryset = CSHost.objects.all()
#     serializer_class = CSHostSerializer


# class EVOwnerList(generics.ListCreateAPIView):
#     queryset = Driver.objects.all()
#     serializer_class = EVOwnerSerializer
 

# class EVOwnerDetail(generics.RetrieveUpdateDestroyAPIView):
#     lookup_field = 'nk'
#     lookup_url_kwarg = 'ev_owner_nk'
#     queryset = Driver.objects.all()
#     serializer_class = EVOwnerSerializer


class EVList(generics.ListCreateAPIView):
    queryset = EV.objects.all()
    serializer_class = EVSerializer


class EVDetail(generics.ListCreateAPIView):
    lookup_field = 'nk'
    lookup_url_kwarg = 'ev_nk'
    queryset = EV.objects.all()
    serializer_class = EVSerializer
