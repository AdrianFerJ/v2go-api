from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import ChargingStation, CSHost, EVOwner, EV

""" 
    Serializers
"""
class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Passwords must match.')
        return data

    def create(self, validated_data):
        data = {
            key: value for key, value in validated_data.items()
            if key not in ('password1', 'password2')
        }
        data['password'] = validated_data['password1']
        return self.Meta.model.objects.create_user(**data)

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'username', 'password1', 'password2',
            'first_name', 'last_name',
        )
        read_only_fields = ('id',)


class ChargingStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargingStation
        fields = '__all__'
        read_only_fields = ('id', 'nk', 'geo_location')


class CSHostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSHost
        fields = ('nk', 'name')


class EVOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EVOwner
        fields = ('nk', 'name', 'latitude', 'longitude')


class EVSerializer(serializers.ModelSerializer):
    class Meta:
        model = EV
        fields = ('nk', 'model', 'manufacturer', 'year', 'charger_type', 'ev_owner', 'calendar')