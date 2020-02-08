from django.db import models
from django.contrib.auth.models import User
from datetime import date,time,datetime

class Muser(models.Model):
    user = models.ForeignKey( User,on_delete=models.CASCADE)
    contact = models.IntegerField(default=0)
    lcount = models.IntegerField(default=0)
    # category = models.IntegerField(default=0)No need
    isadmin = models.IntegerField(default=0) #1-admin 0-user 2-artist
    image = models.ImageField(upload_to='images/songtype/',default='',blank=True, null=True)
  
    def __str__(self):
        return self.user.username + '/'+ str(self.id)


class Songtype(models.Model):
    name = models.CharField(max_length=20,default="")
    image = models.ImageField(upload_to='images/songtype/',default='',blank=True, null=True)

    def __str__(self):
        return self.name 

class Songgenre(models.Model):
    songtype = models.ForeignKey( Songtype,on_delete=models.CASCADE)
    name = models.CharField(max_length=15,default="")
    image = models.ImageField(upload_to='images/songgenre/',default='',blank=True, null=True)
    
    def __str__(self):
        return self.name


class Artist(models.Model):
    artistid = models.AutoField(primary_key=True)
    user = models.ForeignKey( User,on_delete=models.CASCADE)
    artistname = models.CharField(max_length=50, default='artist',unique=False)
    songcount = models.IntegerField(default=0)
    age = models.IntegerField(default=0)
    songtype = models.ForeignKey(Songtype, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/artist/',default='',blank=True, null=True)
    sampleaudio = models.FileField(upload_to='sample/',default='', blank=True, null=True)
    status = models.IntegerField(default=0) # (0-notapproved,1-approved)as artist 

    def __str__(self):
        return self.artistname

class Song(models.Model):
    user = models.ForeignKey( User,on_delete=models.CASCADE)
    songid = models.AutoField(primary_key=True)
    songname = models.CharField(max_length=200,default='song')
    songlength = models.IntegerField(default=0)
    songtype = models.ForeignKey(Songtype, on_delete=models.CASCADE)
    songgenre = models.ForeignKey(Songgenre, on_delete=models.CASCADE)
    document = models.FileField(upload_to='document/',default='', blank=True, null=True)


    def __str__(self):
        return self.songname 
        
class Tour(models.Model):
    user = models.ForeignKey( User,on_delete=models.CASCADE)
    tourid = models.AutoField(primary_key=True)
    city = models.CharField(max_length=30,default='-')
    date = models.DateField()
    # time = models.TimeField()
    day = models.CharField(max_length=10,default='-')
    eventname = models.CharField(max_length=50,default='-')
    timestamp = models.DateTimeField(default = datetime.now, blank=True)
    address = models.CharField(max_length=100,default="")
    tourimage = models.ImageField(upload_to='images/tour/',default='',blank=True, null=True)

    def __str__(self):
        return self.eventname

class Playlist(models.Model):
    user = models.ForeignKey( User,on_delete=models.CASCADE)
    song = models.ForeignKey( Song,on_delete=models.CASCADE)

    