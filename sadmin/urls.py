from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.adminpage,name='adminhome'),
    path('artistdash',views.admindash,name='dash'),
    path('artistDetails/<artist_id>', views.artistDetails, name='artistDetails'),
    path('artistDetails/final/', views.final, name='final'),
    path('tourdash',views.tourdash),
    path('songdash',views.songdash),
    path('followdash',views.followdash),
    path('type',views.utype),
    path('genre',views.ugenre),
    path('uploadtype',views.uploadtype),
    path('uploadgenre',views.uploadgenre)
   
   
]