from django.shortcuts import render
from .models import ChargingStation
from rest_framework import generics, permissions, status, views, viewsets

from main.models import ChargingStation
from .serializers import ChargingStationSerializer # , UserSerializer, GeoCStationSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import mixins
from rest_framework import generics

""" 
    Views
"""
class ChargingStationList(generics.ListCreateAPIView):
    #TODO enable create by changing inheritance from ListAPIView to ListCreateAPIView
    #TODO add permission_classes = (permissions.IsAuthenticated,) AND TEST
    #TODO host can only see her own CS, but no CSs owned by another host
    queryset = ChargingStation.objects.all()
    serializer_class = ChargingStationSerializer


class ChargingStationDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'nk'
    lookup_url_kwarg = 'cs_nk'
    queryset = ChargingStation.objects.all()
    serializer_class = ChargingStationSerializer
