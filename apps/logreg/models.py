# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import bcrypt
# Create your models here.

class UserManager(models.Manager):
    def register(self, first, username, hired, password, confirm):
        response = {
            "valid": True,
            "errors": [],
            "user": None
        }

        if len(first) < 1:
            response['errors'].append('First name cannot be empty')
        elif len(first) < 3:
            response['errors'].append('Name must be at least 3 characters')
        # check if this line works
        elif first.isalpha() == False:
            response['errors'].append('First name can only contain letters')
        
        if len(username) < 1:
            response['errors'].append('Username name cannot be empty')
        elif len(username) < 3:
            response['errors'].append('Username Name must be at least 3 characters')
        elif username.isalpha() == False:
            response['errors'].append('Username name can only contain letters')

        if len(hired) < 1:
            response['errors'].append('Please enter valid hire date')
        
        if len(password) < 1:
            response['errors'].append('Password cannot be empty')           
        elif len(password) < 8:
            response['errors'].append('Password must be at least 8 characters')
        # elif password.isalpha() == False:
        #     response['errors'].append('Password can only contain letters') 

        if len(confirm) < 1:
            response['errors'].append('Please confirm password')
        elif confirm != password:
            response['errors'].append('Passwords must match')

        if len(response['errors']) > 0:
            response['valid'] = False
        else:
            response['user'] = User.objects.create(
                first=first,
                username=username,
                hired=hired,
                password=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            )
        return response

    def login(self, username, password):
        response = {
            "valid": True,
            "errors": [],
            "user": None
        }

        if len(username) < 1:
            response['errors'].append('Username cannot be empty')
        else:
            # print User.objects.filter
            # print User.objects.all()[0].username
            username_list = User.objects.filter(username__iexact=username)
            if len(username_list) == 0:
                response['errors'].append('No username match')

        if len(password) < 1:
            response['errors'].append('Password cannot be empty')           
        elif len(password) < 8:
            response['errors'].append('Password must be at least 8 characters')

        if len(response['errors']) == 0:
            hashed_pw = username_list[0].password
            if bcrypt.checkpw(password.encode(), hashed_pw.encode()):
                response['user'] = username_list[0]
            else:
                response['errors'].append('Incorrect password')
        
        if len(response['errors']) > 0:
            response['valid'] = False
        
        # print User.objects.all()[0].username
        return response

class User(models.Model):
    first = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    hired = models.DateField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()