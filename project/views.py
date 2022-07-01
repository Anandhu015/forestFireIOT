import datetime
import os
import json
import re
from django.shortcuts import HttpResponse
import wave
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from gtts import gTTS
from html5lib import serialize
from django.core import serializers
from django.http import JsonResponse
from .models import Sensor_reading, alert_notify, secondSensor_reading
import telegram 
from django.conf import settings
from pathlib import Path

from gtts import gTTS


# Create your views here.
def startpage_view(request):
    return render(request,"frontpage.html")
def home_view(request):
    return render(request,"home.html")
def about_view(request):
    return render(request,"about.html")
@csrf_exempt
def sensor_data_view(request):
    if request.method == 'POST':
       
        data=request.body.decode('utf-8')
        dict = json.loads(data)
        print(dict)
        try:
            id = dict['device_id']
            temp = dict['temp_reading']
            print(temp)
            hum = dict['hum_reading']
            status = dict['device_status']
            smoke = dict['smoke_reading']
            
            Sensor_reading.objects.create(device_id=id, temp_reading=temp, hum_reading=hum, device_status=status, gas_analog_reading=smoke)
        except:

            data=request.body.decode('utf-8')
            dict = json.loads(data)
            print(dict)
            id1=dict['device_id']
            temp1 = dict['temp_reading1']
            print(temp1)
            hum1 = dict['hum_reading1']
            gas_analog1 = dict['gas_analog_reading1']
            device_status=dict['device_status']
            if device_status == '1':
                status=True
            else:
                status=False
            print(status)
            
            secondSensor_reading.objects.create(device_id1=id1, temp_reading1=temp1, hum_reading1=hum1,device_status1=status, gas_analog_reading1=gas_analog1)
            
    
    if request.accepts("application/json"):
        obj=Sensor_reading.objects.last()
        device_id=obj.device_id
        temp_reading=obj.temp_reading
        hum_reading=obj.hum_reading
        smoke_reading=obj.gas_analog_reading
        device_status=obj.device_status
        print(device_status)
        obj1=secondSensor_reading.objects.last()
        device_id1=obj1.device_id1
        temp_reading1=obj1.temp_reading1
        hum_reading1=obj1.hum_reading1
        smoke_reading1=obj1.gas_analog_reading1
        device_status1=obj1.device_status1
        response={"id":device_id,"temp":temp_reading,"hum":hum_reading,"smoke":smoke_reading,"status":device_status,"id1":device_id1,"temp1":temp_reading1,"hum1":hum_reading1,"smoke1":smoke_reading1,"status1":device_status1}
        
        
    
                

            # Import the required module for text
    # to speech conversion
            
            # os.system("mpg321 welcome.mp3")

            # welcome=open(r"welcome.mp3",'rb')
            # # welcome_sound=welcome.readframes(-1)
            
            # bot.sendVoice(
            # chat_id="@%s" % telegram_settings['channel_name'],voice=welcome
            # )
       

    return JsonResponse({"obj":response})


    
    
def masternode_sensor_view(request):
    return render(request,"reading.html")   
def subnode_sensor_view(request):
    return render(request,"subnodereading.html")    
    


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    
def map_view(request):
    obj=Sensor_reading.objects.last()
    return render(request,"map2.html",{"obj":obj})


    

def alert_view(request):
    obj=Sensor_reading.objects.last()
    id=obj.device_id
    temp=float(obj.temp_reading)
    hum=float(obj.hum_reading)
    smoke = float(obj.gas_analog_reading)
    device_status=obj.device_status
    obj1=secondSensor_reading.objects.last()
    device_id1=obj1.device_id1
    temp_reading1=obj1.temp_reading1
    hum_reading1=obj1.hum_reading1
    smoke_reading1=obj1.gas_analog_reading1
    device_status1=obj1.device_status1
    now = datetime.datetime.now()
    time=now.strftime('%I:%M:%S')
   

  
  
    if temp>20 and smoke>1000:
                val=alert_notify.objects.create(notify_detail="Alert!!!!!!"+"\n"+"Device_id:"+str(id), read_by=False,device_id=id,alert_time=time)
               
                value1="device_id:"+str(id)+"\n"+"temperature_value:"+str(temp)+"\n"+"humidity_value:"+str(hum)+"\n"+"smoke_sensor_reading:"+str(smoke)+"\n"
                value1+="location:"+request.get_host()+"/map"
                telegram_settings = settings.TELEGRAM
                bot = telegram.Bot(token=telegram_settings['bot_token'])
                bot.send_message(chat_id="@%s" % telegram_settings['channel_name'],
                                text=value1, parse_mode=telegram.ParseMode.HTML)
                response={"id":id,"temp":temp,"hum":hum,"smoke":smoke,"status":device_status}
                
    if temp_reading1>20 and smoke_reading1>1000:
                val=alert_notify.objects.create(notify_detail="Alert!!!!!!"+"\n"+"Device_id:"+str(device_id1), read_by=False,device_id=device_id1,alert_time=time)
                value="device_id:"+str(device_id1)+"\n"+"temperature_value:"+str(temp_reading1)+"\n"+"humidity_value:"+str(hum_reading1)+"\n"+"smoke_sensor_reading:"+str(smoke_reading1)+"\n"
                value+="location:"+request.get_host()+"/map"
                telegram_settings1 = settings.TELEGRAM
                bot1= telegram.Bot(token=telegram_settings1['bot_token'])
                bot1.send_message(chat_id="@%s" % telegram_settings1['channel_name'],
                                text=value, parse_mode=telegram.ParseMode.HTML)
                response1={"id":device_id1,"temp":temp_reading1,"hum":hum_reading1,"smoke":smoke_reading1,"status":device_status1}
                
    
    return JsonResponse({"obj":"nothing"})

                # mytext="Hi ,"+str(request.user)
                # mytext += ".device id:"+str(device_id)+"\n"+".temperature value:"+str(temp_reading)+"\n"+".humidity value:"+str(hum_reading)+"\n"+".smoke sensor reading:"+str(smoke_reading)+"\n"
                # language = 'en'
#get all notification
def alert_notify_view(request):
    data=alert_notify.objects.all().order_by('-id')
    count=alert_notify.objects.count()
    print(count)
    Jsonresponse=serializers.serialize('json',data)
    
    return JsonResponse({"data":Jsonresponse,"count":count})
#mark all notifications
def send_alert_notify_view(request):
    noti=request.GET['notif']
    id=request.GET['id']
    
   
       

    notify=alert_notify.objects.get(pk=noti)
    notify.delete()
   
    return JsonResponse({"device_id":id})
def empty_notify_view(request):
    alert_notify.objects.all().delete() 
    return JsonResponse({"bool":True})


   
    
   
    
  