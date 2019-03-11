from django.db import models
from schedule.models import Calendar

# Create your models here.

# Finder
class User(AbstractUser): 
    pass

# Finder
class ChargingStation(models.Model):
    #TODO: include calendar from reservation
    # calendar 		= models.OneToOneField(Calendar, blank=True, on_delete=models.CASCADE)

# Reservations
class EVCar(models.Model):
    #rename to EVehicle

    #TODO renamte owner to ev_owner


