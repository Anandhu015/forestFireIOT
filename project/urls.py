
from django.urls import path
from . import views

urlpatterns=[
    path(' ',views.home_view,name='home'),
    path('readings',views.sensor_data_view,name='sensor'),
    path('reading/masternode',views.masternode_data_view,name='masternode'),

]