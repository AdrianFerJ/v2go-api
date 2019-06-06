from .models import EventCS, EventEV
from rest_framework import generics, serializers


class EventCSSerializer(serializers.ModelSerializer):
	cs = serializers.CharField(source='cs.name', read_only=True)
	created 		= serializers.DateTimeField(format="%Y-%m-%d %H:%M")
	updated 		= serializers.DateTimeField(format="%Y-%m-%d %H:%M")
	startDateTime	= serializers.DateTimeField(format="%Y-%m-%d %H:%M")
	endDateTime		= serializers.DateTimeField(format="%Y-%m-%d %H:%M")
	
	class Meta:
		model = EventCS
		fields = '__all__'


class EventEVSerializer(serializers.ModelSerializer):
	# event_cs = serializers.CharField(source='event_cs.nk', read_only=True)
	event_cs = EventCSSerializer(many=False, read_only=True)
	ev = serializers.CharField(source='ev.model', read_only=True)

	class Meta:
		model = EventEV
		fields = ('nk', 'event_cs', 'ev', 'ev_owner')
