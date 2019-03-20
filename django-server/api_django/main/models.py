# from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry, fromstr

from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser

from schedule.models import Event, EventRelation, Calendar

from .constants import CHARGER_CHOICES, STATUS_CHOICES
from .helpers import create_hash

import datetime
import hashlib


class User(AbstractUser): 
    pass
    # groups = (RIDER , OWNER  , VOLT_MANAGER (?) )


# class CSHost(models.Model):
#     nk          = models.CharField(blank=True, max_length=32, unique=True, db_index=True)
#     created     = models.DateTimeField(auto_now_add=True)
#     updated     = models.DateTimeField(auto_now=True)
#     name        = models.CharField(max_length=40)

#     def __str__(self):
#         return self.name

#     def save(self, *args, **kwargs):
#         if not self.nk:
#             self.nk = create_hash(self)

#         super().save(*args, **kwargs)


# class Driver(models.Model):
#     nk          = models.CharField(blank=True, max_length=32, unique=True, db_index=True)
#     created     = models.DateTimeField(auto_now_add=True)
#     updated     = models.DateTimeField(auto_now=True)
#     name        = models.CharField(max_length=255, default='')
#     latitude    = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=6)
#     longitude   = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=6)

#     def save(self, *args, **kwargs):
#         if not self.nk:
#             self.nk = create_hash(self)

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.name


class ChargingStation(models.Model):
    """ CS model is shared by all different apps / components of this system"""
    #TODO move const declaratios  (status, charge_level) to a dif file
    AVAILABLE       = 'AVAILABLE'
    RESERVED        = 'RESERVED'
    UNAVAILABLE     = 'UNAVAILABLE'
    OUTOFSERVICE    = 'OUT_OF_SERVICE'
    LEVEL_1         = 'LEVEL_1'
    LEVEL_2         = 'LEVEL_2'
    FASTDC          = 'FAST_DC'

    STATUSES = (
        (AVAILABLE, AVAILABLE),
        (RESERVED, RESERVED),
        (UNAVAILABLE, UNAVAILABLE),
        (OUTOFSERVICE, OUTOFSERVICE),
    )
    CHARGE_LEVEL = (
        (LEVEL_1, LEVEL_1),
        (LEVEL_2, LEVEL_2),
        (FASTDC, FASTDC),
    )

    nk           = models.CharField(blank=True, max_length=32, unique=True, db_index=True)
    name         = models.CharField(max_length=255, blank=True)
    external_id  = models.CharField(max_length=100, blank=True)

    # cs_host      = models.ForeignKey(CSHost, on_delete=models.CASCADE,    default=None)
    calendar     = models.OneToOneField(Calendar, blank=True, null=True, on_delete=models.CASCADE)

    charge_level = models.CharField(max_length=32, choices=CHARGE_LEVEL, default=LEVEL_2)
    tarif_text   = models.CharField(max_length=100, blank=True)

    #TODO need a way (method?) to validate address format with google at instanciation
    #TODO host should not be able to edit after saving (read_only)
    address      = models.CharField(max_length=150, blank=False)     
    
    city         = models.CharField(max_length=50, blank=True)
    province     = models.CharField(max_length=50, blank=True)
    country      = models.CharField(max_length=50, blank=True)
    postal_code  = models.CharField(max_length=10, blank=True)

    #TODO: lat,lng, address should be mandatory (blank=False) before pushing to production
    #      and host should not be able to edit after saving (read_only)
    lat          = models.FloatField(null=True, blank=True) 
    lng          = models.FloatField(null=True, blank=True) 
    geo_location = models.PointField(null=True)

    created      = models.DateTimeField(auto_now_add=True)
    updated      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' % (self.nk, self.address)

    def get_absolute_url(self):
        return reverse('main:cs_detail', kwargs={'cs_nk': self.nk})
    
    def create_geo_location(self):
        self.geo_location = fromstr(f'POINT({self.lng} {self.lat})', srid=4326)

    def save(self, **kwargs):
        if not self.nk:
            now = datetime.datetime.now()
            secure_hash = hashlib.md5()
            secure_hash.update(
                #TODO  add :{self.owner} OR owner_nk OR owner foreign key
                f'{now}:{self.address}'.encode(
                    'utf-8'))
            self.nk = secure_hash.hexdigest()
        if not self.geo_location:
            try:
                self.create_geo_location()
            except:
                #TODO: add test (if lat-lng not valid, etc) and add Log if geolocation not created
                pass

        if not self.calendar:
            self.calendar = Calendar.objects.create(name=self.name, slug=self.nk)

        super().save(**kwargs)

    def __str__(self):
        return self.name


class EV(models.Model):
    nk              = models.CharField(blank=True, max_length=32, unique=True, db_index=True)
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)
    model           = models.CharField(max_length=40)
    manufacturer    = models.CharField(max_length=40)
    year            = models.IntegerField()
    charger_type    = models.CharField(max_length=20, choices=CHARGER_CHOICES, default='a')
    # ev_owner        = models.ForeignKey(Driver, on_delete=models.CASCADE)
    calendar        = models.OneToOneField(Calendar, blank=True, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.nk:
            self.nk = create_hash(self)
        
        if not self.calendar:
            self.calendar = Calendar.objects.create(name=self.model, slug=self.nk)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.model
