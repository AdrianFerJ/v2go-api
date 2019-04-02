from django.db import models
from rest_framework.serializers import ValidationError
from main.models import ChargingStation, EV
from main.constants import STATUS_CHOICES
from main.helpers import create_hash
from schedule.models import Calendar, Event
from django.utils.translation import gettext as _
import datetime


class EventCS(models.Model):
	cs_event_nk		= models.CharField(blank=True, null=True, max_length=32, unique=True, db_index=True)
	created 		= models.DateTimeField(auto_now_add=True)
	updated 		= models.DateTimeField(auto_now=True)
	startDateTime	= models.DateTimeField()
	endDateTime		= models.DateTimeField()
	cs	 			= models.ForeignKey(ChargingStation, on_delete=models.CASCADE)
	status			= models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
	ev_event_id		= models.IntegerField(default=-1)

	def save(self, *args, **kwargs):
		event_cs = EventCS.objects.filter(startDateTime=self.startDateTime, 
								  		  endDateTime=self.endDateTime)
		if self.cs_event_nk is None and event_cs.exists():
			raise ValidationError(_(f'CS Event at {self.startDateTime}-{self.endDateTime} already exists'))

		if self.cs_event_nk is not None:
			self.cs_event_nk = create_hash(self)

		if self.ev_event_id == -1: # not reserved yet

			cs_cal = Calendar.objects.get(id=self.cs.calendar.id)

			data = {
				'title': 'Charging Slot for ' + self.cs.name,
				'start': self.startDateTime,
				'end': self.endDateTime,
				'calendar': cs_cal
			}

			event = Event(**data)
			event.save()
			cs_cal.events.add(event)

		elif self.ev_event_id != -1 and self.status == 'AVAILABLE': # about to be reserved
			self.status = 'RESERVED'

		super().save(*args, **kwargs)

	def __str__(self):
		return str(self.cs.name) + ' ' + str(self.status) + ' ' + str(self.startDateTime) + '/' + str(self.endDateTime)


class EventEV(models.Model):
	nk 			= models.CharField(blank=True, null=True, max_length=32, unique=True, db_index=True)
	created 	= models.DateTimeField(auto_now_add=True)
	updated 	= models.DateTimeField(auto_now=True)
	cs_event 	= models.ForeignKey(EventCS, on_delete=models.CASCADE)
	ev 			= models.ForeignKey(EV, on_delete=models.CASCADE)

	def save(self, *args, **kwargs):
		if not self.nk:
			self.nk = create_hash(self)
		
		if self.cs_event.status != 'r':
			data = {
				'title': 'Charging Time for ' + str(self.ev) + str(self.cs_event.cs.name),
				'start': self.cs_event.startDateTime,
				'end': self.cs_event.endDateTime,
				'calendar': self.ev.calendar
			}

			event = Event(**data)
			event.save()
			self.cs_event.ev_event_id = event.id
			self.cs_event.save()
			self.ev.calendar.events.add(event)
		else:
			raise ValidationError(_('EV event already reserved'))

		super().save(*args, **kwargs)

	def __str__(self):
		return str(self.ev) + ' and ' + str(self.cs_event.cs.name) + ' at ' + str(self.cs_event.startDateTime) + '/' + str(self.cs_event.endDateTime)
