from django.db import models
from django.utils import timezone

# Create your models here.

class TripItem(models.Model):
    trip_name = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
<<<<<<< HEAD
    
    def __str__(self):
        return f"{self.trip_name}: due {self.date}"
=======

class userModel(models.Model) :
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    salt = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
>>>>>>> b29a611bf6b1589830268e3862a27c1ebd8438a4
