from django.contrib import admin
from . models import Muser,Artist,Song,Songgenre,Songtype,Tour,Playlist,Follow
# Register your models here.
admin.site.register(Muser)

admin.site.register(Artist)

admin.site.register(Songtype)

admin.site.register(Songgenre)

admin.site.register(Song)

admin.site.register(Tour)

admin.site.register(Playlist)

admin.site.register(Follow)
