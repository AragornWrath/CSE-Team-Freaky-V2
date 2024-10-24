from django.contrib import admin
<<<<<<< HEAD
from .models import TripItem

admin.site.register(TripItem)
=======
import home.models
>>>>>>> b29a611bf6b1589830268e3862a27c1ebd8438a4
# Register your models here.

admin.site.register(home.models.userModel)