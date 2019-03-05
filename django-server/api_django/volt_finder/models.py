import datetime
import hashlib 

# from django.db import models
from django.contrib.gis.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.geos import GEOSGeometry


class User(AbstractUser):
    pass

class ChargingStation(models.Model):
    """ Charging station data model """
    AVAILABLE = 'AVAILABLE'
    RESERVED = 'RESERVED'
    UNAVAILABLE = 'UNAVAILABLE'
    OUTOFSERVICE = 'OUT_OF_SERVICE'
    STATUSES = (
        (AVAILABLE, AVAILABLE),
        (RESERVED, RESERVED),
        (UNAVAILABLE, UNAVAILABLE),
        (OUTOFSERVICE, OUTOFSERVICE),
    )

    nk = models.CharField(max_length=32, unique=True, db_index=True)
    name = models.CharField(max_length=255, default='')
    status = models.CharField(max_length=20, choices=STATUSES, default=UNAVAILABLE)
    manager_id =models.IntegerField() #TODO: this should be a foreign key to link with cs_owner model
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Location is an Address (str)... for now
    location = models.CharField(max_length=255) # TODO: figure how to adequatetly store location (string 
                                                # .. address, LatLng-cordinate, or Lat and Long separate)
    geo_location = models.PointField(null=True, blank=True)    
    address = models.CharField(max_length=100, default='')                                         
    lon = models.FloatField(default=0.0)
    lat = models.FloatField(default=0.0)
    

    def __str__(self):
        return self.nk

    def get_absolute_url(self):
        return reverse('cStation:cStation_detail', kwargs={'cStation_nk': self.nk})

    def save(self, **kwargs):
        if not self.nk:
            now = datetime.datetime.now()
            secure_hash = hashlib.md5()
            secure_hash.update(
                f'{now}:{self.location}:{self.manager_id}'.encode(
                    'utf-8'))
            self.nk = secure_hash.hexdigest()
        super().save(**kwargs)