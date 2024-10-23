from django.db import models

# Create your models here.
class userModel(models.Model) :
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    salt = models.CharField(max_length=100)
    token = models.CharField(max_length=100)

