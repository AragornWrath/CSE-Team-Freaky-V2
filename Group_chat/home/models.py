from django.db import models
from django.utils import timezone

# Create your models here.

class TripItem(models.Model):
    trip_name = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
