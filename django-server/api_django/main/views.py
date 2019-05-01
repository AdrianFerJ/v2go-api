from django.contrib.auth import get_user_model, login, logout

from main.models import ElectricVehicle as EV, ChargingStation as CS, User
from main.serializers import ChargingStationSerializer, UserSerializer, ElectricVehicleSerializer
from volt_reservation.models import EventEV
from volt_reservation.serializers import EventEVSerializer
from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

""" 
    Views
"""
class SignUpView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class LogInView(views.APIView):
    serializer_class = UserSerializer

    def post(self, request):
        user = User.objects.get(username=request.data.get('username'))
        login(request, user=user)
        return Response(self.serializer_class(user).data)


class LogOutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, *args, **kwargs):
        logout(self.request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChargingStationViewSet(viewsets.ModelViewSet):
    #TODO host can only see her own CS, but no CSs owned by another host
    lookup_field = 'nk'
    lookup_url_kwarg = 'station_nk'

    # permission_classes = (permissions.IsAuthenticated,)
    queryset = CS.objects.all()
    serializer_class = ChargingStationSerializer

class ElectricVehicleViewSet(viewsets.ModelViewSet):
    lookup_field = 'nk'
    lookup_url_kwarg = 'ev_nk'

    permission_classes = (permissions.IsAuthenticated,)
    queryset = EV.objects.all()
    serializer_class = ElectricVehicleSerializer


class UserProfile(views.APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user
        user_serializer = UserSerializer(user)

        cars = EV.objects.filter(ev_owner=user.id)
        ev_serializer = ElectricVehicleSerializer(cars, many=True)
        
        reservations = EventEV.objects.filter(ev_owner=user.id)
        reservation_serializer = EventEVSerializer(reservations, many=True)

        return Response({
            'user': user_serializer.data,
            'evs': ev_serializer.data,
            'reservations': reservation_serializer.data,
        })