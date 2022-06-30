from django.db import models
from sqlalchemy import true

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
    
    def __str__(self):
        return(self.notify_detail)
