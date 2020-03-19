from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from music.models import Muser,Artist,Song,Songgenre,Songtype,Tour,Playlist,Follow
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
            rejectMail(artist.artistname,artist.muser.user.email)
            
        elif reject==None:
            print(approve)
            artist.status = 1
    
            muser.isadmin = 2
            artist.save()
            muser.save()
            acceptMail(artist.artistname,artist.muser.user.email)
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

def acceptMail(name,email):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Accepted as an artist"
    msg['From'] = 'harmonymusic1213@gmail.com'
    msg['To'] = email
	
    html = """
		<html>		  
		  <body>
		    <h1 style='color:red'>Accept</h1>
		    <hr>
		    <b>Welcome {0} to Harmony </b>
		    <br>
            Congratulations! You are now a verified artist at Harmony Music.<br>
		    <br>
		    As an artist Harmony gives you the opportunity to showcase your talent,
		    also you can stream music, upload your songs along with the information
		    related to tours and other events absolutely FREE.
		    #goHARMONY 
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
    

def rejectMail(name,email):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Rejected as an artist"
    msg['From'] = 'harmonymusic1213@gmail.com'
    msg['To'] = email
	
    html = """
		<html>		  
		  <body>
		    <h1 style='color:red'>REJECT</h1>
		    <hr>
		    <b>{0}, </b>
		    <br>
            Sorry ,You are no longer a member of Harmony Artist.
		    Try applying again.
		    #goHARMONY
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