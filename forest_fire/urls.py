"""forest_fire URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from project.views import  alert_notify_view, custom_alert_view, graph_view, myhomepage,alertmap_view, device_id_view, empty_notify_view, home, login, logout, send_alert_notify_view,sensor_data_view, map_view,home_view,alert_view,masternode_sensor_view, startpage_view, subnode_sensor_view
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('homepage',home_view,name='home_view'),
    path('home',home,name='home_view'),
    path('readings',sensor_data_view,name='sensor'),
    path('weathermap',map_view,name='map'),
    path('alertmap',alertmap_view,name="alertmap"),
    path('alert',alert_view,name='alert'),
    path('clearall',empty_notify_view,name="empty_notify"),
    path('masternode',masternode_sensor_view,name='masternode'),
    path('subnode',subnode_sensor_view,name='map2'),
    path('startpage',startpage_view,name='start'),
    path('notify',alert_notify_view,name='alert_notify'),
    path('sendnotify',send_alert_notify_view,name="mark_read_notif"),
     path('',login,name="login"),
     path('logout',logout,name="login"),
     path('device',device_id_view,name="device_id"),
     path('myhomepage',myhomepage,name="myhomepage"),
     path("graph",graph_view,name="graph"),
      path("customalert",custom_alert_view,name="custom_alert")
     
      
    


]
