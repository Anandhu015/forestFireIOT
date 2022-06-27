from django.contrib import admin

# Register your models here.
from .models import Sensor_reading, login, secondSensor_reading
admin.site.register(Sensor_reading)
admin.site.register(secondSensor_reading)
admin.site.register(login)