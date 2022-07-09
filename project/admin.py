from django.contrib import admin

# Register your models here.
from .models import Sensor_reading, alert_notify, login, secondSensor_reading,node_alert_values
admin.site.register(Sensor_reading)
admin.site.register(secondSensor_reading)
admin.site.register(login)
admin.site.register(alert_notify)
admin.site.register(node_alert_values)