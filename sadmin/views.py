from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from music.models import Muser,Artist,Song,Songgenre,Songtype,Tour,Playlist,Follow

def checkAdmin(id):
    user = User.objects.get(id = id)
    muser = Muser.objects.get(user = user)
    if muser.isadmin == 1:
        return False
    else:
        return True


def adminpage(req):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
        if checkAdmin(req.user.id):
            return redirect('/music/login')

        return render(req,'shome.html')
    
def admindash(req):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
        if checkAdmin(req.user.id):
            return redirect('/music/login')

        artist = Artist.objects.all().order_by()[::-1] 
        context = {'artists':artist}
        print(artist)
        return render(req, 'admindash.html', context)

def artistDetails(request, artist_id):
    if not request.user.is_authenticated:
        return redirect('/music/login')
    else:
        if checkAdmin(request.user.id):
            return redirect('/music/login')

        artist = Artist.objects.get(artistid=artist_id)
        return render(request, 'artistDetails.html',{'artists':artist})

def final(request):
    if request.method == 'POST':
        aid = request.POST.get('aid')
        approve = request.POST.get('approve')
        reject = request.POST.get('reject')
        artist = Artist.objects.get(artistid=aid)
        muser = Muser.objects.get(id = artist.muser.id)
        print(muser)
        if approve==None:
            print(reject)
            artist.status = -1
            muser.isadmin = 0

            artist.save()
            muser.save()

        elif reject==None:
            print(approve)
            artist.status = 1
    
            muser.isadmin = 2
            artist.save()
            muser.save()
            print(artist.muser.isadmin)
    return redirect('dash')

def tourdash(req):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
        if checkAdmin(req.user.id):
            return redirect('/music/login')

        tour = Tour.objects.all().order_by()[::-1] 
        context = {'tours':tour}
        print(tour)
        return render(req,'tourdash.html',context)

def songdash(req):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
        if checkAdmin(req.user.id):
            return redirect('/music/login')

        song = Song.objects.all().order_by()[::-1] 
        context = {'songs':song}
        print(song)
        return render(req,'songdash.html',context)

def followdash(req):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
        if checkAdmin(req.user.id):
            return redirect('/music/login')

        follow = Follow.objects.all().order_by()[::-1] 
        context = {'follows':follow}
        print(follow)
        return render(req,'followdash.html',context)

def utype(req):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
        if checkAdmin(req.user.id):
            return redirect('/music/login')

        return render(req,'type.html')

def ugenre(req):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
        if checkAdmin(req.user.id):
            return redirect('/music/login')

        songtype = Songtype.objects.all() 
        return render(req,'ugenre.html',{'songtype':songtype})

def uploadtype(req):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
        if req.method == 'POST':
            name = req.POST['sname']
            image = req.FILES['image']
            songtype = Songtype(name=name,image=image)
            songtype.save()
            return redirect('/sadmin/genre')
        return redirect('/sadmin/type')
    
def uploadgenre(req):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
        if req.method == 'POST':
            name = req.POST['gname']
            image = req.FILES['image']
            songtype = req.POST['stype']
            st = Songtype.objects.get(name=songtype)
        
            songgenre = Songgenre(name=name,image=image,songtype=st)
            songgenre.save()
            return redirect('/sadmin/genre')
        return redirect('/sadmin/')
    