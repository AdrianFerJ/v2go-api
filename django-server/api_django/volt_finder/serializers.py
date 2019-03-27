from django.contrib.auth import get_user_model
from rest_framework import serializers
from main.models import ChargingStation


class GeoCStationSerializer(serializers.Serializer):
    """Serialized CS with GEO information """
    nk = serializers.CharField(max_length=32)
    destination_addresses = serializers.CharField(max_length=200)
    duration_txt = serializers.CharField(max_length=100)
    duration_val = serializers.IntegerField()
    distance_txt = serializers.CharField(max_length=100)
    distance_val = serializers.IntegerField()
    status = serializers.CharField(max_length=50)