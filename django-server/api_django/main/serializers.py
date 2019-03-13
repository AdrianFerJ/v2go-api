from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import ChargingStation

class ChargingStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargingStation
        fields = '__all__'
        read_only_fields = ('id', 'nk', 'geo_location')

#TODO: merge from reservations

# class EVOwnerSerializer(serializers.ModelSerializer):

# class EVCarSerializer(serializers.ModelSerializer):

# class CSOwnerSerializer(serializers.ModelSerializer):


# class CSSerializer(serializers.ModelSerializer):