from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.admindash,name='dash'),
    path('artistDetails/<artist_id>', views.artistDetails, name='artistDetails'),
    path('artistDetails/final/', views.final, name='final'),
   
   
]