from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from main.models import ElectricVehicle as EV, ChargingStation as CS, User
from main.serializers import ChargingStationSerializer, UserSerializer, ElectricVehicleSerializer
from volt_reservation.models import EventEV
from volt_reservation.serializers import EventEVSerializer
from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.views import APIView


""" 
    Views
"""


class SignUpView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class AuthTokenLoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'id': user.pk,
            'token': token.key,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            # 'group': user.group,
            
        })


class LogOutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, *args, **kwargs):
        logout(self.request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChargingStationViewSet(viewsets.ModelViewSet):
    # TODO host can only see her own CS, but no CSs owned by another host
    lookup_field = 'nk'
    lookup_url_kwarg = 'station_nk'

    permission_classes = (permissions.IsAuthenticated,)
    queryset = CS.objects.all()
    serializer_class = ChargingStationSerializer


class ElectricVehicleViewSet(viewsets.ModelViewSet):
    lookup_field = 'nk'
    lookup_url_kwarg = 'ev_nk'

    permission_classes = (permissions.IsAuthenticated,)
    queryset = EV.objects.all()
    serializer_class = ElectricVehicleSerializer


class DriverProfileView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, user_id=None, format=None):
        user = User.objects.get(id=user_id)
        user_serializer = UserSerializer(user)

        vehicles = EV.objects.filter(ev_owner=user_id)
        ev_serializer = ElectricVehicleSerializer(vehicles, many=True)

        reservations = EventEV.objects.filter(ev__in=vehicles)
        reservation_serializer = EventEVSerializer(reservations, many=True)

        return Response({
            'user': user_serializer.data,
            'evs': ev_serializer.data,
            'reservations': reservation_serializer.data,
        })
