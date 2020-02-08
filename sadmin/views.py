from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from music.models import Muser,Artist,Song,Songgenre,Songtype,Tour,Playlist

def admindash(req):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:

        artist = Artist.objects.all().order_by()[::-1] 
        context = {'artists':artist}
        print(artist)
        return render(req, 'admindash.html', context)

def artistDetails(request, artist_id):
    if not request.user.is_authenticated:
        return redirect('/music/login')
    else:
        artist = Artist.objects.get(artistid=artist_id)
        return render(request, 'artistDetails.html',{'artists':artist})

def final(request):
    if request.method == 'POST':
        aid = request.POST.get('aid')
        approve = request.POST.get('approve')
        reject = request.POST.get('reject')
        artist = Artist.objects.get(artistid=aid)
        if approve==None:
            print(reject)
            artist.status = -1
            artist.save()
            
        elif reject==None:
            print(approve)
            artist.status = 1
            artist.save()
    return redirect('dash')
