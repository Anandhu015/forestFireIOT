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

from project.views import about_view, alert_notify_view, empty_notify_view, send_alert_notify_view,sensor_data_view, map_view,home_view,alert_view,masternode_sensor_view, startpage_view, subnode_sensor_view
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home',home_view,name='home'),
    path('readings',sensor_data_view,name='sensor'),
    path('map',map_view,name='map'),
    path('alert',alert_view,name='alert'),
    path('clearall',empty_notify_view,name="empty_notify"),
    path('masternode',masternode_sensor_view,name='masternode'),
    path('subnode',subnode_sensor_view,name='map2'),
    path('',startpage_view,name='map2'),
    path('notify',alert_notify_view,name='alert_notify'),
    path('sendnotify',send_alert_notify_view,name="mark_read_notif"),
]
