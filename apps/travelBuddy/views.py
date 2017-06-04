# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect

from .models import User, Trip

from django.contrib import messages


# Create your views here.
### These are all user-related views

def index(request):
    return render(request, 'travelBuddy/index.html')

# Register Users
def register(request):
    if request.method == "POST":
        response = User.objects.check_reg(request.POST)
        if response[0]:
            request.session['user'] = {
                'id': response[1].id,
                'fname': response[1].fname,
                'lname': response[1].lname,
            }
        else:
            for error in response[1]:
                messages.add_message(request, messages.ERROR, error, extra_tags='danger')
            return redirect('/')
    return redirect('/travels')

# Log in Users
def login(request):
    if request.method == "POST":
        response = User.objects.check_login(request.POST)
        if response[0]:
            request.session['user'] = {
                'id': response[1].id,
                'fname': response[1].fname,
                'lname': response[1].lname,
            }
        else:
            for error in response[1]:
                messages.add_message(request, messages.ERROR, error, extra_tags='danger')
            return redirect('/')
        return redirect('/travels')

# Log out users
def logout(request):
    request.session.flush()
    return redirect('/')

### Trip related views are here

# display logged in user's trips and all other trips
def travels(request):
    context = {
        'user_trips': Trip.objects.get_trips(request.session['user']['id']),
        'other_trips': Trip.objects.exclude(id__in=Trip.objects.get_trips(request.session['user']['id'])),
    }
    return render(request, 'travelBuddy/trips.html', context)

# display form for adding trips
def add(request):
    return render(request, 'travelBuddy/add.html')

# process new trips
def process(request):
    if request.method == "POST":
        response = Trip.objects.check_trip(request.POST, request)
        if not response[0]:
            for error in response[1]:
                messages.add_message(request, messages.ERROR, error, extra_tags='danger')
            return redirect('/add')
    return redirect('/destination/{}'.format(response[1].id))

# delete a specific trip
def delete_trip(request, id):
    t = Trip.objects.get(id=id)
    t.delete()
    messages.add_message(request, messages.SUCCESS, 'You have successfully deleted your trip to {}.'.format(t.destination))
    return redirect('/travels')

# join a trip created by another user
def join_trip(request, id):
    t = Trip.objects.get(id=id)
    t.joined_by.add(User.objects.get(id=request.session['user']['id']))
    messages.add_message(request, messages.SUCCESS, 'You have successfully joined a trip to {}.'.format(t.destination))
    return redirect('/travels')

# display trip details
def destination(request, id):
    context = {
        'trip': Trip.objects.get(id=id),
        'logged_user': User.objects.get(id=request.session['user']['id'])
    }
    return render(request, 'travelBuddy/trip.html', context)
