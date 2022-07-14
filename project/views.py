import datetime
import os
import json
import re
from wsgiref import headers
from aiohttp import Payload
from django.shortcuts import HttpResponse
import wave
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from flask import request_finished
from html5lib import serialize
from django.core import serializers
from django.http import JsonResponse
from requests import session

from .models import Sensor_reading, alert_notify, node_alert_values, secondSensor_reading
import telegram 
from django.conf import settings
from pathlib import Path
import numpy as num
import pyrebase


Config = {
 "apiKey": "AIzaSyD_WKNAk8uWk8fP88nOehfKs6CE9ZvDy4A",
  "authDomain": "forest-fire-detection-6605a.firebaseapp.com",
  "databaseURL": "https://forest-fire-detection-6605a-default-rtdb.firebaseio.com",
  "projectId": "forest-fire-detection-6605a",
  "storageBucket": "forest-fire-detection-6605a.appspot.com",
  "messagingSenderId": "2411392518",
  "appId": "1:2411392518:web:ab0ec58c5c81e1ac485d87",
  "measurementId": "G-KP4XMVH4CD"
}
firebase=pyrebase.initialize_app(Config)
authe = firebase.auth()
database=firebase.database()

def login(request):
    return render(request,"login.html")
# Create your views here.
def startpage_view(request):
    return render(request,"frontpage.html")
def home(request):
    return render(request,"homepage.html")


@csrf_exempt
def home_view(request):
    email=request.POST.get('email')
    password=request.POST.get('pass')
    print(password)
    print(email)
    try:
        # if there is no error then signin the user with given email and password
        user=authe.sign_in_with_email_and_password(email,password)
        
        
    except:
        message="Invalid Credentials!!Please ChecK your Data"
        return render(request,"Login.html",{"message":message})
    
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    request.session['email']=email
    """
    name=email.split('@')
   
    del name[1]
    name=''.join(map(str,name))
    
    print(name)
    return render(request,"homepage.html",{"name":name})
    """
    return redirect('/myhomepage')


def myhomepage(request):
    #session_id=user['idToken']
    #request.session['uid']=str(session_id)
    email = request.session['email']
    name=email.split('@')
    del name[1]
    name=''.join(map(str,name))
    
    print("name:"+name)
    return render(request,"homepage.html",{"name":name})


def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    return render(request,"login.html")
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

# def map_view(request):
  
#     return render(request,"map2.html")



    
@csrf_exempt
def alert_view(request):
     if request.method == 'POST':
       
        data=request.body.decode('utf-8')
        dict = json.loads(data)
        now = datetime.datetime.now()
        time=now.strftime("%I:%M:%S")
        print(dict)
        try:

            id=dict['device_id']
            temp=float(dict['temp_reading'])
            hum=float(dict['hum_reading'])
            smoke=int(dict['smoke_reading'])
            status=dict['device_status']
           
            if temp is not None  and  hum is not None and smoke is not None :
                  
        
            
                        val=alert_notify.objects.create(notify_detail="Alert!!!!!!"+"\n"+"Device_id:"+str(id), read_by=False,device_id=id,alert_time=time)
                        alert=node_alert_values.create(device_id=id,temp_reading=temp,hum_reading=hum,device_status=status,gas_analog_reading=smoke)
                        value1="device_id:"+str(id)+"\n"+"temperature_value:"+str(temp)+"\n"+"humidity_value:"+str(hum)+"\n"+"smoke_sensor_reading:"+str(smoke)+"\n"
                        value1+="location:"+request.get_host()+"/weathermap"+"?q="+id
                        telegram_settings = settings.TELEGRAM
                        bot = telegram.Bot(token=telegram_settings['bot_token'])
                        bot.send_message(chat_id="@%s" % telegram_settings['channel_name'],
                                        text=value1, parse_mode=telegram.ParseMode.HTML)
                        response={"id":id,"temp":temp,"hum":hum,"smoke":smoke,"status":status}
            else:
                print("error")
        except:
            id=dict['device_id']
            temp=float(dict['temp_reading1'])
            hum=float(dict['hum_reading1'])
            smoke=int(dict['gas_analog_reading1'])
            status=dict['device_status']
            if  temp is  not None and hum is not None and smoke is not  None :          
            
                        val=alert_notify.objects.create(notify_detail="Alert!!!!!!"+"\n"+"Device_id:"+str(id), read_by=False,device_id=id,alert_time=time)
                        alert=node_alert_values.create(device_id=id,temp_reading=temp,hum_reading=hum,device_status=status,gas_analog_reading=smoke)
                        value="device_id:"+str(id)+"\n"+"temperature_value:"+str(temp)+"\n"+"humidity_value:"+str(hum)+"\n"+"smoke_sensor_reading:"+str(smoke)+"\n"
                        value+="location:"+request.get_host()+"/weathermap"+"?q="+id
                        telegram_settings1 = settings.TELEGRAM
                        bot1= telegram.Bot(token=telegram_settings1['bot_token'])
                        bot1.send_message(chat_id="@%s" % telegram_settings1['channel_name'],
                                        text=value, parse_mode=telegram.ParseMode.HTML)
                        # response1={"id":device_id1,"temp":temp_reading1,"hum":hum_reading1,"smoke":smoke_reading1,"status":device_status1}
            else:
                print("error")
        
                    
    
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
@csrf_exempt
def send_alert_notify_view(request):
    noti=request.GET['notif']
    
    
    notify=alert_notify.objects.get(pk=noti)
    notify.delete()
    # if id ==1:
    #     return render(request,"map2.html",{"obj":id})
    # elif id==2:
    #     return render(request,"map2.html",{"obj":id})
    # else:
    return JsonResponse({"obj":"got value"})
def empty_notify_view(request):
    alert_notify.objects.all().delete() 
    return JsonResponse({"bool":True})

def alertmap_view(request):
 
    return render(request,"alertmap.html")


@csrf_exempt
def device_id_view(request):
    id=request.POST.get('device_id')
    print(id)
    # request.session['mapid'] = id
    # if request.accepts("application/json"):
        # if id ==1:
        #     return JsonResponse({"obj":id})
        # elif id==2:
        #     return JsonResponse({"obj":id})
        # else:
        #     return JsonResponse({"obj":"error"})
    return JsonResponse({"obj":id})
        # return render(request,"map2.html",{"obj":id})


def map_view(request):
    # id = request.session['mapid']
    # print("id"+id)
    # id=int(id)
    # print(type(id))
    # print(+"This is id")
    return render(request,"map2.html",{"id":id,"device_id":request.GET['device_id']})

def graph_view(request):
    return render(request,"graph.html")   
    
def custom_alert_view(request):
    message=request.GET['message']
    if message=='':
        pass
    else:
        update="Important update from ADMIN !!!!!!!!!!"
        
        update+="\n**************************************\n"
        
        telegram_settings1 = settings.TELEGRAM
        bot1= telegram.Bot(token=telegram_settings1['bot_token'])
        bot1.send_message(chat_id="@%s" % telegram_settings1['channel_name'],text=update+message, parse_mode=telegram.ParseMode.HTML)
    return JsonResponse({"hi":message})  
    
  