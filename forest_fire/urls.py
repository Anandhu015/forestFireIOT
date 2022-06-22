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

from project.views import about_view,sensor_data_view, map_view,home_view,alert_view,masternode_sensor_view, subnode_data_view, subnode_sensor_view
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_view,name='home'),
    path('readings',sensor_data_view,name='sensor'),
    path('subnodereadings',subnode_data_view,name='sub-sensor'),
    path('map',map_view,name='map'),
    path('alert',alert_view,name='alert'),
    path('about',about_view,name='about'),
    path('masternode',masternode_sensor_view,name='masternode'),
     path('subnode',subnode_sensor_view,name='map2'),
]
