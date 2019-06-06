from django.contrib.auth import get_user_model
from rest_framework import serializers
from main.models import ChargingStation


class CSwithDistanceSerializer(serializers.ModelSerializer):
    """Serialized CS with GEO information """
    distance_to_poi = serializers.SerializerMethodField()  #.FloatField()

    def get_distance_to_poi(self, obj):
        return obj.distance_to_poi.m

    class Meta:
        model = ChargingStation
        fields = '__all__'
        # fields = ('id', 'nk', 'distance_to_poi' )
        read_only_fields = ('id', 'nk', 'geo_location')
