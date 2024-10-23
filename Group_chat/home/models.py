from django.db import models
from django.utils import timezone

# Create your models here.

class TripItem(models.Model):
    trip_name = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)

class userModel(models.Model) :
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    salt = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
