from collections import OrderedDict
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from main.constants import USERNAME, PASSWORD, U_DRIVER, U_OWNER, FIRST_NAME, LAST_NAME


def create_user(username=USERNAME, password=PASSWORD,
                group=U_DRIVER, first_name=FIRST_NAME,
                last_name=LAST_NAME):
    user = get_user_model().objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password
    )

    Group.objects.get_or_create(name=username)

    return user


def filter_by_cs_event_nk(cs_event, query):
    return list(filter(lambda event_cs: event_cs['nk'] == cs_event.nk, query))


def cs_event_to_ordered_dict(cs_event):
    return OrderedDict([
        ('id', cs_event.id),
        ('cs', cs_event.cs.name),
        ('created', cs_event.created.strftime('%Y-%m-%d %H:%M')),
        ('updated', cs_event.updated.strftime('%Y-%m-%d %H:%M')),
        ('startDateTime', cs_event.startDateTime.strftime('%Y-%m-%d %H:%M')),
        ('endDateTime', cs_event.endDateTime.strftime('%Y-%m-%d %H:%M')),
        ('nk', cs_event.nk),
        ('status', cs_event.status),
        ('ev_event_id', cs_event.ev_event_id)
    ])


def ev_event_to_ordered_dict(ev_events):
    ev_events_serialized = []

    for ev_event in ev_events:
        ev_events_serialized.append(OrderedDict([
            ('nk', ev_event.nk),
            ('event_cs', cs_event_to_ordered_dict(ev_event.event_cs)),
            ('ev', ev_event.ev.model),
            ('ev_owner', ev_event.ev_owner.pk)
        ]))

    return ev_events_serialized


def evs_to_ordered_dict(evs):
    evs_serialized = []

    for ev in evs:
        evs_serialized.append(OrderedDict([
            ('nk', ev.nk),
            ('model', ev.model),
            ('nickname', ev.nickname),
            ('manufacturer', ev.manufacturer),
            ('year', ev.year),
            ('charger_type', ev.charger_type),
            ('ev_owner', ev.ev_owner.pk),
            ('calendar', ev.calendar.pk)
        ]))

    return evs_serialized
