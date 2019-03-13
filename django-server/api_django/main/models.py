# from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry, fromstr

from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser

import datetime
import hashlib 


# Create your models here.

# Finder
class User(AbstractUser): 
    pass
    # groups = (RIDER , OWNER  , VOLT_MANAGER (?) )


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

    nk           = models.CharField(max_length=32, unique=True, db_index=True)
    name         = models.CharField(max_length=255, blank=True)
    external_id  = models.CharField(max_length=100, blank=True)
    #TODO: this should be a foreign key to link with cs_owner model
    # cs_host   = models.IntegerField()

    CHARGE_LEVEL = (
        (LEVEL_1, LEVEL_1),
        (LEVEL_2, LEVEL_2),
        (FASTDC, FASTDC),
    )
    charge_level = models.CharField(max_length=32, choices=CHARGE_LEVEL, default=LEVEL_2)
    tarif_text   = models.CharField(max_length=100, blank=True)

    address      = models.CharField(max_length=150) 
    location     = models.CharField(max_length=150, default='') 
    city         = models.CharField(max_length=50, blank=True)
    province     = models.CharField(max_length=50, blank=True)
    country      = models.CharField(max_length=50, blank=True)
    postal_code  = models.CharField(max_length=10, blank=True)
    #TODO: lat,lng should be mandatory (blank=False) before pushing to production
    lat          = models.FloatField(null=True, blank=True) 
    lng          = models.FloatField(null=True, blank=True) 
    geo_location = models.PointField(null=True)

    created      = models.DateTimeField(auto_now_add=True)
    updated      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nk

    def get_absolute_url(self):
        return reverse('main:host_cs_detail', kwargs={'cs_nk': self.nk})
    
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
        super().save(**kwargs)

# Finder
# class ChargingStation(models.Model):
#     #TODO: include calendar from reservation
#     # calendar 		= models.OneToOneField(Calendar, blank=True, on_delete=models.CASCADE)

# # Reservations
# class EVCar(models.Model):
#     #rename to EVehicle

#     #TODO renamte owner to ev_owner
# 