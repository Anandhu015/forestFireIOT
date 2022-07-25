from datetime import datetime,date
from email.policy import default
import django
from django.db import models
from django.forms import TimeField
from django.utils import timezone
from sqlalchemy import true
default=datetime.now()
time=default.strftime("%H:%M:%S")
hour=default.hour
minute=default.minute
seconds=default.second
from datetime import date

alert_date = date.today()

# Create your models here.
class Sensor_reading(models.Model):
    device_id=models.IntegerField()
    temp_reading=models.FloatField(max_length=20,null=true)
    hum_reading=models.FloatField(max_length=20,null=true)
    device_status=models.BooleanField(default=True)
    gas_analog_reading=models.FloatField(max_length=20,default="0",null=true)
    

class secondSensor_reading(models.Model):
    device_id1=models.IntegerField()
    temp_reading1=models.FloatField(max_length=20,null=true)
    hum_reading1=models.FloatField(max_length=20,null=true)
    device_status1=models.BooleanField(default=True)
    gas_analog_reading1=models.FloatField(max_length=20,default="0",null=true)

class login(models.Model):
    user_id=models.IntegerField(primary_key=true)
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
class alert_notify(models.Model):
    notify_detail=models.TextField()
    read_by=models.BooleanField(default=False)
    device_id=models.IntegerField(default=1)
    
    alert_time=models.TimeField(default=time)
   
    
    def __str__(self):
        return(self.notify_detail)
class node_alert_values(models.Model):
    device_id=models.IntegerField()
    temp_reading=models.FloatField(max_length=20)
    hum_reading=models.FloatField(max_length=20)
    device_status=models.BooleanField(default=True)
    gas_analog_reading=models.FloatField(max_length=20)
    alert_time=models.TimeField(default=time)
    alert_date=models.DateField(default=django.utils.timezone.now)
    

