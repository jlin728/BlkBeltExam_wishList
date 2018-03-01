# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ..logreg.models import User
from datetime import datetime

# Create your models here.

class ItemManager(models.Manager):
    def add(self, post_data, owner):
        errors = []
        x = len(post_data['name']) 
        if x < 1:
            errors.append('Item name cannot be empty')
        elif x < 3:
            errors.append('Name must be at least 3 characters')
        
        if len(errors) > 0 :
            print errors
            return(False, errors)
        else:
            additem = Item.objects.create(
                name = post_data['name'],
                created_by_id = owner
            )            
            return (True, additem)

    def like(self,item_id,id):
        a = Item.objects.get(id=item_id)
        b = User.objects.get(id=id)
        a.all_customers.add(b)            
        return {}

    def remove(self,item_id,id):
        a = Item.objects.get(id=item_id)
        b = User.objects.get(id=id)
        a.all_customers.remove(b)            
        return {}
    
    def delete(self,item_id,id):
        Item.objects.filter(id=item_id).delete()
        return {}

class Item(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name = 'owner')
    all_customers = models.ManyToManyField(User, related_name = 'liked')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ItemManager()