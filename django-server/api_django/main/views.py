from django.shortcuts import render
from .models import ChargingStation

from rest_framework import generics, permissions, status, views#, viewsets

from main.models import ChargingStation
from .serializers import ChargingStationSerializer # , UserSerializer, GeoCStationSerializer


class ChargingStationListView(generics.ListAPIView):
    #TODO enable create by changing inheritance from ListAPIView to ListCreateAPIView
    queryset = ChargingStation.objects.all()
    serializer_class = ChargingStationSerializer
