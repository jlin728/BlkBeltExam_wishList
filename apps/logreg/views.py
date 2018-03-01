# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "logreg/index.html")


def register(request):
    # print "registration working"
    # print request.POST
    response = User.objects.register(
        request.POST['first'],
        request.POST['username'],
        request.POST['hired'],
        request.POST['password'],
        request.POST['confirm']
    )
    print response
    if response['valid']:
        request.session['user_id'] = response['user'].id
        return redirect('/dashboard')
        # redirect to dashboard in list_app
    else:
        for error_message in response['errors']:
            messages.add_message(request, messages.ERROR, error_message)
        return redirect("/")


def login(request):
    # print "login working"
    response = User.objects.login(
        request.POST['username'],
        request.POST['password'],
    )
    if response['valid']:
        request.session['user_id'] = response['user'].id
        
        return redirect('/dashboard')
        # redirect to dashboard in list_app
    else:
        for error_message in response['errors']:
            print error_message
            messages.add_message(request, messages.ERROR, error_message)
        return redirect("/")

def logout(request):
    request.session.clear()
    return redirect('/')
