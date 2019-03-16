from .models import CSEvent, EVEvent
from rest_framework import generics, serializers


class CSEventSerializer(serializers.ModelSerializer):
	cs = serializers.CharField(source='cs.nk', read_only=True)

	class Meta:
		model = CSEvent
		fields = '__all__'


class EVEventSerializer(serializers.ModelSerializer):
	class Meta:
		model = EVEvent
		fields = ('nk', 'cs_event', 'ev')