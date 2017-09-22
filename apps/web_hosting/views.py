# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from models import Website

# Create your views here.
def index(request):
    return render(request,"web_hosting/index.html")

def process(request):

    if request.POST['web_site'].startswith('www.') and request.POST['web_site'].endswith('.com') and Website.objects.filter(name=request.POST['web_site']).exists() == False:
        Website.objects.create(name=request.POST['web_site'])
        return redirect('/display')

    elif Website.objects.filter(name=request.POST['web_site']).exists() == True:
        messages.error(request, " Site, already in Database")
        return redirect ('/')

    else:
        messages.error(request,"Site needs to start with 'www' and end with '.com'")
        return redirect ('/')


def check(request):

    if Website.objects.filter(name=request.POST['name']).exists() == True:
        messages.error(request," No, this name is already in use")

    elif request.POST['name'].startswith('www.') == False or request.POST['name'].endswith('.com') == False:
        messages.error(request," Name should start with 'www' and end with '.com'")

    else:
        messages.success(request, "Yes, name is available")

    return redirect ('/')

def display(request):
    context = {
        "sites":Website.objects.all()
    }
    return render(request,"web_hosting/display.html", context)

def clear(request):
    Website.objects.all().delete()
    return redirect ('/')
