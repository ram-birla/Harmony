from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #landing page
    path('',views.landingpage),
    path('about/',views.aboutpage),
    path('info/',views.infopage),
    path('contact/',views.contactpage),
    # login/register (user)(artist)
    path("login/",views.userlogin),
    path("register/",views.register),
    path("reg",views.reg),
    path("log",views.login),
    # logout
    path('logout',views.logout),
    # homepage user,artist
    path("home/",views.homePage),
    # add song (artist)(admin)
    path('home/adsong/',views.upload),
    path('run/',views.simple_upload),
    # tour form (artist)(admin)
    path('home/tourpage/',views.tourpage),
    path('toursub/',views.toursub),
    # tour page (both)
    path('tourdetail/',views.tourdetails),
    # application for an artist (user)
    path('home/applypage/',views.applypage),
    path('applysub/',views.applysub),
    # songgenre page (user,artist)
    path('home/genre/<stype_id>',views.genre,name='genre'),
    path('home/genre/song/<sgenre_id>',views.musicpage,name='song'),
    # artist page song (user,artist)
    path('artist/',views.artistpage),
    # artistprofile pge
    path('artist/artistprofile/<artist_id>',views.artistprofile,name='artistprofile'),
    # Artist follow and unfollow
    path('artist/artistprofile/follow/<artist_id>',views.follow),
    path('artist/artistprofile/unfollow/<artist_id>',views.unfollow),
    # my playlist page
    path('home/myplaylist/',views.myplaylist),
    path('home/myprofile/',views.myprofile,name='myprofile'),
    #add to playlist
    path('home/myplaylist/add/<song_id>',views.addToPlaylist),
    #increase click count
    path('home/myplaylist/click/<song_id>',views.increaseClickCount),
    #remove from playlist
    path('home/myplaylist/remove/<song_id>',views.removeFromPlaylist),
    #search music
    # path('home/genre/song/search',views.search,name='search'),
    #shuffle music in genre
    path('home/genre/song/shuffle/<sgenre_id>',views.sshuffle,name='shuffle'),
    # shuffle song in artist
    path('home/artist/artistprofile/shuffle/<artist_id>',views.ashuffle),
    # shuffle song in myplaylist
    path('home/myplaylist/shuffle/',views.myshuffle),
]