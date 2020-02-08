from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, auth
from . models import Muser,Artist,Song,Songgenre,Songtype,Tour,Playlist
# Create your views here.
def register(req):
    return render(req,"register.html")

def userlogin(req):
    return render(req,"login.html")

def reg(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        username = email
        password1 = request.POST['pass1']
        password2 = request.POST['pass2']                                       
        contact = request.POST['phone']
        # category = request.POST['type']
        print(username,email,contact)  
        
        if password1==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'email already taken')
                return redirect('/music/register')
            else:
                user = User.objects.create_user(username=username, email=email, password = password1, first_name = password1, last_name = name)
                muser = Muser(user_id=user.id, contact=contact)
                print('creating user....')
                user.save()
                muser.save()
                print('user created')
                user = auth.authenticate(username=username,password=password1)
                if user is not None:
                    auth.login(request,user)
                    return redirect("/music/login")
                else:
                    return redirect('register')
        else:
            messages.info(request,'password not matched')
            return redirect('/music/register')
    else:
        return redirect('/music/register')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email,password)
        try:
            # cuser = User.objects.get(email=email)
            # print(cuser)
            # cseller = Seller.objects.get(user_id=cuser.id)
            user = auth.authenticate(username=email, password=password)
            muser = Muser.objects.get(user_id=user.id)
            print("---------------------------")
            print(user,muser)
            print("---------------------------")
            if user is not None:
               
                if muser.isadmin == 1:
                    auth.login(request,user)
                    return redirect('/sadmin/')
                elif muser.isadmin == 2:
                    auth.login(request,user)
                    c = muser.lcount + 1
                    muser.lcount = c
                    print(muser.lcount)
                    muser.save()
                    return redirect('/music/artisthome')
                else:
                    auth.login(request,user)
                    c = muser.lcount + 1
                    muser.lcount = c
                    print(muser.lcount)
                    muser.save()
                    return redirect('/music/home')

            else:
                return redirect('/music/login')
        except:
            print('except')
            return redirect('/music/login')

    else:
        return redirect('/music/login')


def logout(request):
    auth.logout(request)
    return redirect('/music/login')

def homePage(req):
    # print(req.user.id)
    songtypes = Songtype.objects.all()
    songgenres = Songgenre.objects.all()
    songs = Song.objects.all()
    context = {'songtype' : songtypes,
        'songgenre' : songgenres,
        'song': songs
    }
    return render(req,'home.html',context)

def artisthome(req):
    songtypes = Songtype.objects.all()
    context = {'songtype' : songtypes
    }
    return render(req,'artisthome.html',context)

def upload(request):
    
    if not request.user.is_authenticated:
        return redirect('/music/register')
    else:
        songtypes = Songtype.objects.all()
        songgenres = Songgenre.objects.all()
        context = {'songtypes' : songtypes,
        'songgenres' : songgenres,
        }
        return render(request,"upload.html",context)

def simple_upload(req):
    uid=req.user.id
    song = User.objects.get(id=uid)
    print(uid,song)
    if req.method == 'POST' and req.FILES['myfile']:
        songtype = req.POST['stype']
        songgenre = req.POST['sgenre']
        myfile = req.FILES['myfile']
        print(songtype,songgenre)
        print(myfile)
        st = Songtype.objects.get(name=songtype)
        sg = Songgenre.objects.get(name=songgenre)
        
        # fs = FileSystemStorage()
        # document = fs.save(myfile.name,myfile)
        # uploaded_file_url = fs.url(document)
        song = Song(user=song,songname = (myfile.name).split('.')[0],songtype = st,songgenre = sg,document = myfile)
        song.save()
        return render(req,'upload.html',{
            'file_status' : 'uploaded'
        })

    return render(req,'upload.html')

def tourpage(req):
    return render(req,'tour.html')

def toursub(req):
    uid=req.user.id
    tour = User.objects.get(id=uid)
    print(uid,tour)
    if req.method == 'POST':
        eventname = req.POST['eventname']
        city = req.POST['city']
        day = req.POST['day']
        date = req.POST['date']
        address = req.POST['address']
        image = req.POST['photo']
        print(eventname,city,day,date)

        tour = Tour(user=tour,city = city, date = date,day=day,eventname=eventname,address=address,tourimage=image)
        tour.save()
        return render(req,'tour.html',{
            'file_status' : 'uploaded'
        })

    return render(req,'tour.html')

def tourdetails(req):
    tours = Tour.objects.all()
    context = { 'tour' : tours}
    return render(req,'tourpage.html',context) 

 
def applypage(req):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
        songtypes = Songtype.objects.all()
        context = {'songtypes' : songtypes
        }
    return render(req,'apply.html',context)

def applysub(req):
    uid=req.user.id
    artist = User.objects.get(id=uid)
    if req.method == 'POST' and req.FILES['samplefile']:
        name = req.POST['name']
        age = req.POST['age']
        songtype = req.POST['stype']
        samplefile = req.FILES['samplefile']
        image = req.FILES['image']
        st = Songtype.objects.get(name=songtype)
       
        artist = Artist(user=artist,artistname = name,age=age,songtype=st,image=image,sampleaudio=samplefile)
        artist.save()
        return render(req,'apply.html',{
            'file_status' : 'uploaded'
        })

    return render(req,'/music/home')

def artistpage(req):
    artists = Artist.objects.filter(status=1)
    context = {'artist': artists}
    return render(req,'artist.html',context)

def genre(req, stype_id):
    songtype = Songtype.objects.get(id=stype_id)
    songgenres = Songgenre.objects.filter(songtype=songtype)
    context = {
        'songgenre': songgenres,
    }
    return render(req,'genre.html',context)

def musicpage(req, sgenre_id):
    songgenre = Songgenre.objects.get(id=sgenre_id)
    songs = []
    for songgenres in songgenre:
        song = Song.objects.filter(songgenre=songgenres)
        for s in song:
            songs.append(s)
    context={
        'songs':songs,
    }

    print(songs)    
    return render(req,'music.html',context)

def artistprofile(req):
    return render(req,'artprofile.html')

def myplaylist(req):
    return render(req,'myplay.html')