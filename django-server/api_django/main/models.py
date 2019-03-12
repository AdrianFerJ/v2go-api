from django.db import models
from django.contrib.auth.models import AbstractUser, Group


# Create your models here.

# Finder
class User(AbstractUser): 
    pass

#     #User = models.OneToOneField(User, related_name="main_user", primary_key=True)
#     # groups = models.OneToOneField(Group, related_name="main_groups", primary_key=True)
#     #related_name argument to the definition for 'VoltUser.groups' or 'User.groups'


# Finder
# class ChargingStation(models.Model):
#     #TODO: include calendar from reservation
#     # calendar 		= models.OneToOneField(Calendar, blank=True, on_delete=models.CASCADE)

# # Reservations
# class EVCar(models.Model):
#     #rename to EVehicle

#     #TODO renamte owner to ev_owner
