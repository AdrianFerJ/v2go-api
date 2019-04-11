from .models import EventCS, EventEV
from rest_framework import generics, serializers


class EventCSSerializer(serializers.ModelSerializer):
	cs = serializers.CharField(source='cs.nk', read_only=True)

	class Meta:
		model = EventCS
		fields = '__all__'


class EventEVSerializer(serializers.ModelSerializer):
	event_cs = serializers.CharField(source='event_cs.nk', read_only=True)
	ev = serializers.CharField(source='ev.nk', read_only=True)

	class Meta:
		model = EventEV
		fields = ('nk', 'event_cs', 'ev')
