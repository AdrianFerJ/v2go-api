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

class ChargingStationList(generics.ListAPIView):
    #TODO enable create by changing inheritance from ListAPIView to ListCreateAPIView
    queryset = ChargingStation.objects.all()
    serializer_class = ChargingStationSerializer


# class ChargingStationDetail(viewsets.ReadOnlyModelViewSet):  
#     """ Get's a32char nk and returns CS's detail info that matches the nk """
    # lookup_field = 'nk'
    # lookup_url_kwarg = 'cs_nk'
#     permission_classes = (permissions.IsAuthenticated,)
#     queryset = ChargingStation.objects.all()
#     serializer_class = ChargingStationSerializer


class ChargingStationDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'nk'
    lookup_url_kwarg = 'cs_nk'
    queryset = ChargingStation.objects.all()
    serializer_class = ChargingStationSerializer


# class ChargingStationDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = ChargingStation.objects.all()
#     serializer_class = ChargingStationSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)