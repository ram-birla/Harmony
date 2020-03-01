from django.shortcuts import render,redirect
from django.http import HttpResponse
def home(req):
    return redirect("/music/")