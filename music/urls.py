from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # login/register (user)(artist)
    path("login/",views.userlogin),
    path("register/",views.register),
    path("reg",views.reg),
    path("log",views.login),
    # logout
    path('logout',views.logout),
    # homepage user
    path("home/",views.homePage),
    # homepage artist
    path("artisthome/",views.artisthome),
    # add song (artist)(admin)
    path('adsong/',views.upload),
    path('run/',views.simple_upload),
    # tour form (artist)(admin)
    path('tourpage/',views.tourpage),
    path('toursub/',views.toursub),
    # tour page (both)
    path('tourdetail/',views.tourdetails),
    # application for an artist (user)
    path('applypage/',views.applypage),
    path('applysub/',views.applysub),
    # songgenre page (user,artist)
    path('home/genre/<stype_id>',views.genre,name='genre'),
    path('home/music/<sgenre_id>',views.musicpage,name='song'),
    # artist page song (user,artist)
    path('artist/',views.artistpage),
    # myprofile pge
    path('artistprofile/',views.artistprofile),
    # my playlist page
    path('myplaylist/',views.myplaylist),


]