# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def validate(self, postData):
        results = {
            'status': True,
            'errors':[]
        }

        # check to see if first_name and last_name are actually
        # characters and not spaces
        if len(postData['first_name']) < 3:
            results['errors'].append('First Name is too short')
            results['status'] = False
        if len(postData['last_name']) < 3:
            results['errors'].append('Last Name is too short')
            results['status'] = False
        if not re.match("[^@]+@[^@]+\.[^@]+", postData['email']):
            results['errors'].append('Email is not valid.')
            results['status'] = False
        if postData['password'] != postData['confirm']:
            results['errors'].append('Passwords needs to be at least 5 characters long')
            results['status'] = False
        if len(postData['password']) < 5:
            results['errors'].append('Password is not long enough')
            results['status'] = False
        if len(self.filter(email=postData['email'])) > 0:
            results['errors'].append('User already exists')
            results['status'] = False
        if postData['first_name'].isalpha() == False:
            results['errors'].append('First Name needs to be lettters')
            results['status'] = False
        if postData['last_name'].isalpha() == False:
            results['errors'].append('Last Name needs to be lettters')
            results['status'] = False


        return results

    def creator(self,postData):
        user = self.create(
            first_name=postData['first_name'],
            last_name=postData['last_name'],
            email=postData['email'],
            password=bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()),
        )
        return user

    def loginval(self,postData):
        results = {
            'status': True,
            'error': [],
            'user': None
        }

        users = self.filter(email=postData['email'])
        if len(users) < 1:
            results['status'] = False
        else:
            if bcrypt.checkpw(postData['password'].encode(), users[0].password.encode()):
                results['user'] = users[0]
            else:
                results['status'] = False
        return results

class User(models.Model):
    first_name = models.CharField(max_length=255)

    last_name = models.CharField(max_length=255)

    email = models.CharField(max_length=255)

    password = models.CharField(max_length=255)

    objects = UserManager()
