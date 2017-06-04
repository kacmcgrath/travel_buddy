# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q

from django.db import models

import re

import bcrypt

from bcrypt import hashpw, gensalt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
PW_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}$')

# Create your models here.

### User models and managers here

class UserManager(models.Manager):
    # validated registration data for new users
    def check_reg(self, postData):
        response = []
        errors = []
        if not len(postData['fname']) > 2:
            errors.append("First name must be longer than 2 characters.")
        if not len(postData['lname']) > 2:
            errors.append("Last name must be longer than 2 characters.")
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("Please enter a valid email address.")
            if User.objects.filter(email = postData['email']):
                errors.append("User is already registered.  Please log in.")
        if not PW_REGEX.match(postData['pword']):
            errors.append("Password must be at least 8 characters long and contain at least one lowercase letter, one uppercase letter, one number, and one special character.")
        if not postData['pword'] == postData['conf_pword']:
            errors.append("Passwords must match.")
        if errors:
            response.append(False)
            response.append(errors)
        else:
            password = bcrypt.hashpw(postData['pword'].encode(), gensalt())
            response.append(True)
            response.append(User.objects.create(fname=postData['fname'], lname=postData['lname'], email=postData['email'], pword=password))
        return response

    # validates login data for existing users
    def check_login(self, postData):
        response = []
        errors = []
        user = User.objects.filter(email=postData['email']).values()
        if not user or not PW_REGEX.match(postData['pword']):
            errors.append("Username or password is incorrect.")
        else:
            try:
                if not bcrypt.checkpw(postData['pword'].encode(), user[0]['pword'].encode()):
                    errors.append("Username or password is incorrect.")
            except ValueError:
                errors.append("Username or password is incorrect.")
        if errors:
            response.append(False)
            response.append(errors)
        else:
            response.append(True)
            response.append(User.objects.get(email=postData['email']))
        return response

class User(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    pword = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

### Trips models and managers here

class TripManager(models.Manager):
    # Validates trip information when a user enters a new trip & creates the trip
    def check_trip(self, postData, request):
        response = []
        errors = []
        if not len(postData['destination']) > 2:
            errors.append('Destination must be longer than 2 characters.')
        if not len(postData['description']) > 3:
            errors.append('Please enter a description.')
        if not postData['depart_date'] or not postData['return_date']:
            errors.append('Departure and return dates are required.')
        if not postData['depart_date'] < postData['return_date']:
            errors.append('Return date must be after Departure date.')
        if errors:
            response.append(False)
            response.append(errors)
        else:
            trip = Trip.objects.create(destination=postData['destination'], depart_date=postData['depart_date'], return_date=postData['return_date'], planned_by=User.objects.get(id=request.session['user']['id']), description=postData['description'])
            response.append(True)
            response.append(trip)
        return response
    # Gets trip information for trips the logged in user has either planned or joined to display on the main page
    def get_trips(self, user_id):
        return Trip.objects.filter(Q(planned_by=User.objects.get(id=user_id)) | Q(joined_by=User.objects.get(id=user_id)))

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    depart_date = models.DateTimeField()
    return_date = models.DateTimeField()
    planned_by = models.ForeignKey(User, related_name="trips_planned")
    joined_by = models.ManyToManyField(User, related_name="trips_joined")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TripManager()
