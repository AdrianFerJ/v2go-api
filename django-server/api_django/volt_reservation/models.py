from django.db import models
from rest_framework.serializers import ValidationError
from main.models import ChargingStation
from main.models import ElectricVehicle as EV
from main.models import User
from main import constants
from main.helpers import create_hash
from schedule.models import Calendar, Event
from django.utils.translation import gettext as _
import datetime


class EventCS(models.Model):
	nk				= models.CharField(blank=True, null=True, max_length=32, unique=True, db_index=True)
	created			= models.DateTimeField(auto_now_add=True)
	updated			= models.DateTimeField(auto_now=True)
	startDateTime	= models.DateTimeField()
	endDateTime		= models.DateTimeField()
	cs				= models.ForeignKey(ChargingStation, on_delete=models.CASCADE)
	status			= models.CharField(max_length=20, choices=constants.STATUS_CHOICES, default=constants.AVAILABLE)
	ev_event_id		= models.IntegerField(default=-1)

	def save(self, *args, **kwargs):
		event_cs = EventCS.objects.filter(startDateTime=self.startDateTime,
										  endDateTime=self.endDateTime,
										  cs=self.cs)

		if self.nk is None and event_cs.exists():
			raise ValidationError(_(f'CS Event at {self.startDateTime}-{self.endDateTime} already exists'))

		if self.nk is None:
			self.nk = create_hash(self)

		if self.ev_event_id != -1 and self.status == constants.AVAILABLE: # about to be reserved
			self.status = constants.RESERVED
		elif self.ev_event_id == -1 and self.status == constants.RESERVED: # event getting canceled
			self.status = constants.AVAILABLE

		if self.ev_event_id == -1 and self.status == constants.AVAILABLE: # not reserved yet
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

		super().save(*args, **kwargs)

	def split_event_cs(self, custom_start_datetime, custom_end_datetime):
		"""Split into three different event cs"""
		new_events = []

		if self.is_range_within_event_cs_excluding_start_and_end(custom_start_datetime, custom_end_datetime):
			new_events.append(create_custom_event_cs(self.startDateTime, custom_start_datetime))
			new_events.append(create_custom_event_cs(custom_end_datetime, self.endDateTime))
			self.startDateTime, self.endDateTime = custom_start_datetime, custom_end_datetime
		else:
			start_datetime, end_datetime = self.startDateTime, self.endDateTime
			if self.is_range_within_event_cs_and_starts_at_start_datetime(custom_start_datetime, custom_end_datetime):
				start_datetime, self.endDateTime = (custom_end_datetime,)*2

			elif self.is_range_within_event_cs_and_ends_at_end_datetime(custom_start_datetime, custom_end_datetime):
				self.startDateTime, end_datetime = (custom_start_datetime,)*2
			
			new_events.append(self.create_custom_event_cs(start_datetime, end_datetime))
		
		for new_event in new_events:
			new_event.save()

		self.save()

	def is_range_within_event_cs_excluding_start_and_end(self, start_datetime, end_datetime):
		return self.startDateTime < start_datetime and self.endDateTime > end_datetime

	def is_range_within_event_cs_and_starts_at_start_datetime(self, start_datetime, end_datetime):
		return self.startDateTime == start_datetime and end_datetime < self.endDateTime

	def is_range_within_event_cs_and_ends_at_end_datetime(self, start_datetime, end_datetime):
		return self.startDateTime < custom_start_datetime and custom_end_datetime == self.endDateTime

	def create_custom_event_cs(self, start_datetime, end_datetime):
		return EventCS.objects.create(
				startDateTime=start_datetime,
				endDateTime=end_datetime,
				cs=self.cs,
				status=constants.AVAILABLE
		)

	def __str__(self):
		return str(self.cs.name) + ' ' + str(self.status) + ' ' + str(self.startDateTime) + '/' + str(self.endDateTime)


class EventEV(models.Model):
	nk			= models.CharField(blank=True, null=True, max_length=32, unique=True, db_index=True)
	created		= models.DateTimeField(auto_now_add=True)
	updated		= models.DateTimeField(auto_now=True)
	status		= models.CharField(max_length=20, choices=constants.STATUS_CHOICES, default=constants.RESERVED)
	event_cs	= models.ForeignKey(EventCS, on_delete=models.CASCADE)
	ev			= models.ForeignKey(EV, on_delete=models.CASCADE)
	ev_owner	= models.ForeignKey(User, on_delete=models.CASCADE, null=True)

	def save(self, *args, **kwargs):

		if self.status == constants.CANCELED:
			event = Event.objects.get(id=self.event_cs.ev_event_id)

			self.event_cs.ev_event_id = -1
			self.event_cs.save()
		elif self.event_cs.status != constants.RESERVED:
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
