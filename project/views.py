import os
import json
from django.shortcuts import HttpResponse
import wave
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from gtts import gTTS
from html5lib import serialize
from django.core import serializers
from django.http import JsonResponse
from .models import Sensor_reading, secondSensor_reading
import telegram 
from django.conf import settings
from pathlib import Path

from gtts import gTTS


# Create your views here.
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
            print(device_status)
            secondSensor_reading.objects.create(device_id1=id1, temp_reading1=temp1, hum_reading1=hum1,device_status1=device_status, gas_analog_reading1=gas_analog1)
            
    
    if request.accepts("application/json"):
        obj=Sensor_reading.objects.last()
        device_id=obj.device_id
        temp_reading=obj.temp_reading
        hum_reading=obj.hum_reading
        smoke_reading=obj.gas_analog_reading
        device_status=obj.device_status
        print(device_status)
        response={"id":device_id,"temp":temp_reading,"hum":hum_reading,"smoke":smoke_reading,"status":device_status}
        
        return JsonResponse({"obj":response})


@csrf_exempt
def subnode_data_view(request):
    if request.accepts("application/json"):
        obj=secondSensor_reading.objects.last()
        device_id=obj.device_id1
        temp_reading=obj.temp_reading1
        hum_reading=obj.hum_reading1
        smoke_reading=obj.gas_analog_reading1
        device_status=obj.device_status1
        response={"id":device_id,"temp":temp_reading,"hum":hum_reading,"smoke":smoke_reading,"status":device_status}
        print(device_status)
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
    obj=Sensor_reading.objects.last();
    id=obj.device_id
    temp=float(obj.temp_reading)
    hum=float(obj.hum_reading)
    smoke = float(obj.gas_analog_reading)
    
    if temp>20 and smoke>0:
        value="device_id:"+str(id)+"\n"+"temperature_value:"+str(temp)+"\n"+"humidity_value:"+str(hum)+"\n"+"smoke_sensor_reading:"+str(smoke)+"\n"
        value+="location:"+request.get_host()+"/map"
        telegram_settings = settings.TELEGRAM
        bot = telegram.Bot(token=telegram_settings['bot_token'])
        bot.send_message(chat_id="@%s" % telegram_settings['channel_name'],
                        text=value, parse_mode=telegram.ParseMode.HTML)
        mytext="Hi ,"+str(request.user)
        mytext += ".device id:"+str(id)+"\n"+".temperature value:"+str(temp)+"\n"+".humidity value:"+str(hum)+"\n"+".smoke sensor reading:"+str(smoke)+"\n"
        language = 'en'
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("welcome.mp3")

        # Import the required module for text
# to speech conversion
        
        # os.system("mpg321 welcome.mp3")

        welcome=open(r"welcome.mp3",'rb')
        # welcome_sound=welcome.readframes(-1)
        
        bot.sendVoice(
        chat_id="@%s" % telegram_settings['channel_name'],voice=welcome
        )
       

    
    return render(request,"fire_alert.html",{})