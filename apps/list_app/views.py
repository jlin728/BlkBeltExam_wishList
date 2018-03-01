# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import User, Item
from django.contrib import messages

def dashboard(request):
    if "user_id" not in request.session:
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    data = {
        'user' : user,
        'other_items': Item.objects.exclude(created_by=request.session['user_id']),
        'self_items': Item.objects.filter(created_by=request.session['user_id']),
        'liked_items' : Item.objects.filter(all_customers=request.session['user_id']),
        'all_items' : Item.objects.all(),
    }
    return render(request, 'list_app/index.html', data)

def new(request):
    data = {
         'user' : User.objects.get(id=request.session['user_id']),
         'users': User.objects.all(),
    }
    return render(request, 'list_app/new.html', data)

def add(request):
    response = Item.objects.add(
        request.POST,
        request.session['user_id']
    )
    if response[0] == True:
        # request.session['item_id'] = response['item'].id Can I set sessions for item id here, at creation?
        return redirect('/dashboard')
    else:
        for error_message in response[1]:
            print error_message
            messages.add_message(request, messages.ERROR, error_message)
        return redirect('/wish_item/new')

def like(request, id):
    response = Item.objects.like(id, request.session['user_id']),
    return redirect('/dashboard', response)

def remove(request, id):
    response = Item.objects.remove(id, request.session['user_id']),
    return redirect('/dashboard', response)

def delete(request, id):
    response = Item.objects.delete(id, request.session['user_id']),
    return redirect('/dashboard', response)

def item(request, id):
    data = {
        'this_item' : Item.objects.get(id = id),
        "others": User.objects.filter(liked = id),
        # "others": User.objects.filter(liked = id),        
    }

    return render(request, 'list_app/item.html', data)