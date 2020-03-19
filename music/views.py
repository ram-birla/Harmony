from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, auth
from . models import Muser,Artist,Song,Songgenre,Songtype,Tour,Playlist,Follow
import datetime 
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randint


# Create your views here.
def landingpage(req):
    return render(req,"landing.html")

def aboutpage(req):
    songcount = Song.objects.all().count()
    tourcount = Tour.objects.all().count()
    usercount = User.objects.all().count()
    artistcount = Artist.objects.all().count()
    context = {
        'songcount':songcount,
        'tourcount':tourcount,
        'usercount':usercount,
        'artistcount':artistcount
    }
    
    return render(req,"about.html",context)

def infopage(req):
    songcount = Song.objects.all().count()
    tourcount = Tour.objects.all().count()
    usercount = User.objects.all().count()
    artistcount = Artist.objects.all().count()
    context = {
        'songcount':songcount,
        'tourcount':tourcount,
        'usercount':usercount,
        'artistcount':artistcount
    }
    return render(req,"info.html",context)

def contactpage(req):
    return render(req,"contact.html")

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
        image = request.FILES.get('image')
        # category = request.POST['type']
        print(username,email,contact)  
        
        if password1==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'email already taken')
                return redirect('/music/register')
            else:
                user = User.objects.create_user(username=username, email=email, password = password1, first_name = password1, last_name = name)
                muser = Muser(user_id=user.id, contact=contact,image=image)
                print('creating user....')
                user.save()
                muser.save()
                print('user created')
                sendMail(name,email)
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

def checkmail(request, email_id):
    print(email_id)
    res=''
    if User.objects.filter(email=email_id).exists():
        res = 'email already registered'
        return HttpResponse(res)
    else:
        return HttpResponse('')

# send mail 

def sendMail(name,email):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Registration"
    msg['From'] = 'harmonymusic1213@gmail.com'
    msg['To'] = email
	
    html = """
		<html>		  
		  <body>
		    <h1 style='color:red'>Registration Success!!</h1>
		    <hr>
		    <b>Welcome {0} to Harmony </b>
		    <br>
            Your registration at Harmony is Successfull!<br>
		    Enjoy and Stream High Quality of Songs from your favourite artist and keep sharing.<br>
		    #goHarmony
		    <br><br>
		    Thanks
            <br/>
            Team Harmony
		  </body>
		</html>
		""".format(name)
    part2 = MIMEText(html, 'html')
    msg.attach(part2)


    fromaddr = 'harmonymusic1213@gmail.com'
    toaddrs  = email	
    username = 'harmonymusic1213@gmail.com'
    password = 'asdf13ASDF'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()
 

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email,password)
        try:
            # cuser = User.objects.get(email=email)
            # print(cuser)
            # cseller = Seller.objects.get(user_id=cuser.id)
            print("---------")
            user = auth.authenticate(username=email, password=password)
            print(user)
            muser = Muser.objects.get(user=user)
            print("---------------------------")
            print(user,muser)
            print("---------------------------")
            if user is not None:
               
                if muser.isadmin == 1:
                    auth.login(request,user)
                    return redirect('/sadmin/')
                elif muser.isadmin == 2:
                    auth.login(request,user)
                    print("0")
                    c = muser.lcount + 1
                    print("1")
                    muser.lcount = c
                    print("2")
                    print(muser.lcount)
                    muser.save()
                    print("3")
                    return redirect('/music/home')
                else:
                    auth.login(request,user)
                    c = muser.lcount + 1
                    muser.lcount = c
                    print(muser.lcount)
                    muser.save()
                    return redirect('/music/home')

            else:
                messages.info(request,'Invalid User,Register Yourself')
                return redirect('/music/login')
        except:
            messages.info(request,'Invalid Email or password')
            print('except')
            return redirect('/music/login')

    else:
        messages.info(request,'Check Your Credentials')
        return redirect('/music/login')

def forgotpass(req):
    return render(req,'forgot.html')

def passw(req):
    if req.method == 'POST':
        email = req.POST.get('email')
        print(email)
        try:
            user = User.objects.get(email=email)
            print(user.last_name)
            otp = sendmail(user.last_name,email)
            muser = Muser.objects.get(user=user)
            print(muser)
            muser.otp = otp
            print(muser.otp)
            muser.save()
            return redirect('/music/setpass')
        except:
            messages.info(req,'Email doesn"t exist')
            return redirect('/music/forgotpassword/')
    else:
        return HttpResponse("Failed")
    

def chngpass(req):
    return render(req,"change.html")

def confirmpass(req):
    if req.method == 'POST':
        email = req.POST.get('email')
        otp = req.POST.get('otp')
        password1 = req.POST.get('pass1')
        password2 = req.POST.get('pass2')
        print(password1,password2)
        try:
            if password1==password2:
                print("hgfdxfghj")
                user = User.objects.get(email=email)
                
                muser = Muser.objects.get(user=user,otp=otp)
                print(muser)
                user.first_name = password1
                user.set_password(password1)
                user.save()
                return redirect('/music/login')
            else:
                messages.info(req,'password not matched')
                return redirect('/music/setpass')
        except:
            messages.info(req,'Email entered is incorrect or otp didn"t matched')
            return redirect('/music/setpass')    

def sendmail(name,mail):
    otp = randomdigit(6)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Change Password "
    msg['From'] = 'harmonymusic1213@gmail.com'
    msg['To'] = mail
	
    html = """
		<html>		  
		  <body>
		    <h1 style='color:red'>Change Password</h1>
		    <hr>
		    <b>{0} , </b>
		    <br>
		    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
		    Change Your Passsword using this OTP:<b>{1}</b>.<br><br>
		    Thanks
            <br/>
            Team Harmony
		  </body>
		</html>
		""".format(name,otp)
    part2 = MIMEText(html, 'html')
    msg.attach(part2)


    fromaddr = 'harmonymusic1213@gmail.com'
    toaddrs  = mail	
    username = 'harmonymusic1213@gmail.com'
    password = 'asdf13ASDF'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()
    return otp

def randomdigit(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)    


def logout(request):
    auth.logout(request)
    return redirect('/music/login')

def homePage(req):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
        # print(req.user.id)
        songtypes = Songtype.objects.all()
        songgenres = Songgenre.objects.all()
        songs = Song.objects.order_by('-clickCount')[0:10]
        # artist = Artist.objects.order_by('-songcount')[0:2]
        top = Artist.objects.order_by('-fcount')[0]
        artist = Artist.objects.filter(status=1).order_by('-fcount')[0:10]
        print(artist)
        tops = Song.objects.order_by('-clickCount')[0]
        muser = Muser.objects.get(user = req.user.id)
        
        context = {'songtype' : songtypes,
            'songgenre' : songgenres,
            'song': songs,
            'muser':muser,
            'artist':artist,
            'top':top,
            'tops':tops
        }
        return render(req,'home.html',context)


def upload(request):
    if not request.user.is_authenticated:
        return redirect('/music/register')
    else:
        muser = Muser.objects.get(user = request.user.id)
        songtypes = Songtype.objects.all()
        songgenres = Songgenre.objects.all()
        context = {'songtypes' : songtypes,
        'songgenres' : songgenres,
        'muser':muser
        }
        return render(request,"upload.html",context)

def simple_upload(req):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
        user = User.objects.get(id = req.user.id)
        if req.method == 'POST' and req.FILES['myfile']:
            songtype = req.POST['stype']
            songgenre = req.POST['sgenre']
            myfile = req.FILES['myfile']
            print(songtype,songgenre)
            print(myfile)
            st = Songtype.objects.get(name=songtype)
            sg = Songgenre.objects.get(songtype=st,name=songgenre)
            muser = Muser.objects.get(user = user) 
            artist = Artist.objects.get(muser = muser)
            print(artist)
            c = artist.songcount + 1
            artist.songcount = c
            print(artist.songcount)
            artist.save()
            song = Song(artist=artist,songname = (myfile.name).split('.')[0],songtype = st,songgenre = sg,document = myfile)
            song.save()
            return redirect('/music/home/myprofile/#mysong')

        return render(req,'upload.html',{
                'file_status' : 'not uploaded'
            })

def tourpage(req):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
        muser = Muser.objects.get(user = req.user.id)
        
        return render(req,'tour.html',{'muser':muser})

def toursub(req):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
        uid=req.user.id
        user = User.objects.get(id=uid)
        print(uid,user)
        if req.method == 'POST':
            eventname = req.POST['eventname']
            city = req.POST['city']
            day = req.POST['day']
            date = req.POST['date']
            time = req.POST.get('time')
            print(time)
            address = req.POST['address']
            image = req.FILES['image']
            print(eventname,city,day,date)
            tour = Tour(user=user,city = city, date = date,day=day,time=time,eventname=eventname,address=address,tourimage=image)
            tour.save()
            # return render(req,'tour.html',{
            #     'file_status' : 'uploaded'
            # })
            return redirect('/music/home/myprofile/#mytour')

        return render(req,'tour.html',{
                'file_status' : 'not uploaded'
            })

def tourdetails(req):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
        now = datetime.datetime.now().date()
        tours = Tour.objects.filter(status=0)
        for t in tours:
            tour = Tour.objects.get(tourid = t.tourid)
            print((tour.date - now).days)
            if (tour.date - now).days < 0:
                tour.status = 1
                tour.save()
    
        
        tours = Tour.objects.filter(status=0)
        muser = Muser.objects.get(user = req.user.id)
        context = { 'tour' : tours,
            'muser': muser
        }
        return render(req,'tourpage.html',context) 

 
def applypage(req):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
        muser = Muser.objects.get(user = req.user.id)
        songtypes = Songtype.objects.all()
        context = {'songtypes' : songtypes,
        'muser':muser
        }
    return render(req,'apply.html',context)

def applysub(req):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
        uid=req.user.id
        artist = Muser.objects.get(user=uid)
        if req.method == 'POST' and req.FILES['samplefile']:
            name = req.POST['name']
            age = req.POST['age']
            songtype = req.POST['stype']
            samplefile = req.FILES['samplefile']
            image = req.FILES['image']
            st = Songtype.objects.get(name=songtype)
        
            artist = Artist(muser=artist,artistname = name,age=age,songtype=st,image=image,sampleaudio=samplefile)
            artist.save()
            return render(req,'apply.html',{
                'file_status' : 'uploaded'
            })

        return render(req,'/music/home')

def artistpage(req):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
    
        artists = Artist.objects.filter(status=1)
        muser = Muser.objects.get(user = req.user.id)
        context = {'artist': artists,
            'muser':muser
        }
        return render(req,'artist.html',context)

def genre(req, stype_id):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
        songtype = Songtype.objects.get(id=stype_id)
        songgenres = Songgenre.objects.filter(songtype=songtype)
        muser = Muser.objects.get(user = req.user.id)
        context = {
            'songgenre': songgenres,
            'muser':muser
        }
        return render(req,'genre.html',context)

def musicpage(req, sgenre_id):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
        
        songgenre = Songgenre.objects.get(id=sgenre_id)
        songs = []
        song = Song.objects.filter(songgenre=songgenre)
        muser = Muser.objects.get(user = req.user.id)
    
        context={
            'songs':song,
            'muser':muser,
            'songgenre':songgenre
        }
        
        print(song[0].document)
        
        return render(req,'music.html',context)

def artistprofile(req, artist_id):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
        user = User.objects.get(id = req.user.id)
        muser = Muser.objects.get(user = req.user.id)
        artist = Artist.objects.get(artistid = artist_id)
        followercount = Follow.objects.filter(following = artist).count()
        print(artist)
        try:
            ifollow = Follow.objects.get(following = artist, follower = user)
            print(ifollow)
            if ifollow:
                isfollow = True 
        except:
            isfollow = False
            print('False--------------  ------------')

        # print(isfollow)
        song = Song.objects.filter(artist = artist)
        context = {
            'artist':artist,
            'songs':song,
            'muser':muser,
            'isfollow':isfollow,
            'followercount':followercount
        }
        return render(req,'artprofile.html',context)

def myplaylist(req):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
        muser = Muser.objects.get(user = req.user.id)
        print(muser)
        song = Playlist.objects.filter(user = req.user.id)
        songcount = Playlist.objects.filter(user = req.user.id).count()
        context = {
            'muser':muser,
            'song':song,
            'songcount':songcount,
        }
        return render(req,'myplay.html',context)

def myprofile(request):
    print('Hello')
    if not request.user.is_authenticated:
        return redirect('/music/login')
    else:
        print(request.user.id)
        muser = Muser.objects.get(user = request.user.id)
        print(muser)
        artist = Artist.objects.get(muser = muser)
        print(artist)
        tour = Tour.objects.filter(user = request.user.id)
        tcount = Tour.objects.filter(user = request.user.id).count()
        song = Song.objects.filter(artist = artist)
        print(artist.image)
        for t in tour:
            print(t.eventname)
        for s in song:
            print(s.songname)

        context ={
            'artists':artist,
            'tours':tour,
            'songs':song,
            'muser':muser,
            'tcount':tcount
        }
        return render(request,'myprofile.html',context)

def follow(req, artist_id):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
        uid = req.user.id
        user = User.objects.get(id = uid)
        artist = Artist.objects.get(artistid = artist_id)
        artist.inFcount() 
        print(user,artist)
        #instance upload
        follow = Follow(following = artist, follower = user)
        follow.save()
        artist.save()
        return HttpResponse("DONE")

def unfollow(req, artist_id):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
        uid = req.user.id
        user = User.objects.get(id = uid)
        artist = Artist.objects.get(artistid = artist_id)
        artist.deFcount()
        print(user,artist)
        #instance delete
        follower = Follow.objects.get(following = artist, follower = user)
        follower.delete()
        artist.save()
        return HttpResponse("UNFOLLOWED")

def addToPlaylist(req, song_id):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
        print(song_id)
        user = User.objects.get(id = req.user.id)
        sng = Song.objects.get(songid = song_id)
        try:
            print("ghussa")
            s = Playlist.objects.get(user = user,song=sng)
            print(s.id)
            if s.song == sng:
                
                print("already added")
                return HttpResponse("already added")
            else:
                play = Playlist(user=user,song=sng)
                play.save()    
        except:
            play = Playlist(user=user,song=sng)
            play.save()
        return HttpResponse('Added')

def removeFromPlaylist(req, song_id):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
        print(song_id)
        user = User.objects.get(id = req.user.id)
        song = Song.objects.get(songid = song_id)
        play = Playlist.objects.get(user = user,song=song)
        play.delete()
        return HttpResponse('Deleted')

def increaseClickCount(req, song_id):
    print(song_id)
    song = Song.objects.get(songid = song_id)
    song.inClickCount()
    song.save()
    return HttpResponse(song.clickCount)

# def search(request):
#     if request.method == 'GET':
#         query= request.GET.get('q')

#         submitbutton= request.GET.get('submit')

#         if query is not None:
#             results = Song.objects.filter(songname=query).distinct()
            
#             context={'results': results,
#                      'submitbutton': submitbutton}

#             return render(request, 'music.html', context)

#         else:
#             return render(request, 'search/search.html')

#     else:
#         return render(request, 'search/search.html')

def sshuffle(req, sgenre_id):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
        muser = Muser.objects.get(user = req.user.id)
        songgenre = Songgenre.objects.get(id=sgenre_id)
        song = Song.objects.filter(songgenre=songgenre)
        mylist = list(song)
        for item in mylist:
            print(item.songid)
        print(mylist)
        random.shuffle(mylist)
        for item in mylist:
            print(item.songid)
        print(mylist)
        song = mylist
        context = {
            'muser':muser,
            'songs':song,
            'songgenre':songgenre
        }
        return render(req,'music.html',context)

def ashuffle(req, artist_id):
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
        artist = Artist.objects.get(artistid = artist_id)
        song = Song.objects.filter(artist = artist)
        user = User.objects.get(id = req.user.id)
        muser = Muser.objects.get(user = req.user.id)
        followercount = Follow.objects.filter(following = artist).count()
        print(artist)
        try:
            ifollow = Follow.objects.get(following = artist, follower = user)
            print(ifollow)
            if ifollow:
                isfollow = True 
        except:
            isfollow = False
            print('False--------------  ------------')

        mylist = list(song)
        for item in mylist:
            print(item.songid)
        print(mylist)
        random.shuffle(mylist)
        for item in mylist:
            print(item.songid)
        print(mylist)
        song = mylist
        context = {
            'artist':artist,
            'songs':song,
            'muser':muser,
            'isfollow':isfollow,
            'followercount':followercount
            
        }
        return render(req,'artprofile.html',context)

def myshuffle(req):  
    if not req.user.is_authenticated:
        return redirect('/music/login')
    else:
        muser = Muser.objects.get(user = req.user.id)
        print(muser)
        song = Playlist.objects.filter(user = req.user.id)
        songcount = Playlist.objects.filter(user = req.user.id).count()
        mylist = list(song)
        for item in mylist:
            print(item.song.songid)
        print(mylist)
        random.shuffle(mylist)
        for item in mylist:
            print(item.song.songid)
        print(mylist)
        song = mylist
        
        context = {
            'muser':muser,
            'song':song,
            'songcount':songcount,
        }
        return render(req,'myplay.html',context)


