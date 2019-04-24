from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.decorators import api_view, permission_classes

from main.models import ChargingStation
from main.models import ElectricVehicle as EV, User
from main.serializers import ChargingStationSerializer, UserSerializer, ElectricVehicleSerializer
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


class ChargingStationViewSet(viewsets.ModelViewSet):
    #TODO host can only see her own CS, but no CSs owned by another host
    lookup_field = 'nk'
    lookup_url_kwarg = 'station_nk'

    # permission_classes = (permissions.IsAuthenticated,)
    queryset = ChargingStation.objects.all()
    serializer_class = ChargingStationSerializer


class ElectricVehicleViewSet(viewsets.ModelViewSet):
    lookup_field = 'nk'
    lookup_url_kwarg = 'ev_nk'

    permission_classes = (permissions.IsAuthenticated,)
    queryset = EV.objects.all()
    serializer_class = ElectricVehicleSerializer


@api_view()
@permission_classes((permissions.IsAuthenticated, ))
def my_account(request, user_id):
    user = User.objects.get(id=user_id)
    serializer = UserSerializer(user)
    return Response(serializer.data)
