from django.db import models
from rest_framework.serializers import ValidationError
from main.models import ChargingStation
from main.models import ElectricVehicle as EV
from main.constants import STATUS_CHOICES
from main.helpers import create_hash
from schedule.models import Calendar, Event
from django.utils.translation import gettext as _
import datetime


class EventCS(models.Model):
	nk				= models.CharField(blank=True, null=True, max_length=32, unique=True, db_index=True)
	created 		= models.DateTimeField(auto_now_add=True)
	updated 		= models.DateTimeField(auto_now=True)
	startDateTime	= models.DateTimeField()
	endDateTime		= models.DateTimeField()
	cs	 			= models.ForeignKey(ChargingStation, on_delete=models.CASCADE)
	status			= models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
	ev_event_id		= models.IntegerField(default=-1)

	def save(self, *args, **kwargs):
		event_cs = EventCS.objects.filter(startDateTime=self.startDateTime, 
								  		  endDateTime=self.endDateTime,
								  		  cs=self.cs)

		if self.nk is None and event_cs.exists():
			raise ValidationError(_(f'CS Event at {self.startDateTime}-{self.endDateTime} already exists'))

		if self.nk is None:
			self.nk = create_hash(self)

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
	event_cs 	= models.ForeignKey(EventCS, on_delete=models.CASCADE)
	ev 			= models.ForeignKey(EV, on_delete=models.CASCADE)

	def save(self, *args, **kwargs):
		if self.event_cs.status != 'RESERVED':
			if not self.nk:
				self.nk = create_hash(self)

			data = {
				'title': 'Charging Time for ' + str(self.ev) + str(self.event_cs.cs.name),
				'start': self.event_cs.startDateTime,
				'end': self.event_cs.endDateTime,
				'calendar': self.ev.calendar
			}

			event = Event(**data)
			event.save()
			self.event_cs.ev_event_id = event.id
			self.event_cs.save()
			self.ev.calendar.events.add(event)
		else:
			raise ValidationError(_('EV event already reserved'))

		super().save(*args, **kwargs)

	def __str__(self):
		return str(self.ev) + ' and ' + str(self.event_cs.cs.name) + ' at ' + str(self.event_cs.startDateTime) + '/' + str(self.event_cs.endDateTime)
