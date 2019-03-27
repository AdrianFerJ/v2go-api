from .models import EventCS, EventEV
from rest_framework import generics, serializers


class EventCSSerializer(serializers.ModelSerializer):
	cs = serializers.CharField(source='cs.nk', read_only=True)

	class Meta:
		model = EventCS
		fields = '__all__'


class EventEVSerializer(serializers.ModelSerializer):
	class Meta:
		model = EventEV
		fields = ('nk', 'event_cs', 'ev')
