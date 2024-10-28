from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseNotFound
from django.template import loader, RequestContext
from pymongo import MongoClient
from bcrypt import hashpw, gensalt
from home.generateToken import generateToken
import hashlib
from .models import userModel
from django.http import JsonResponse

from django.views.generic import ListView
from .models import TripItem
from django.core.exceptions import ObjectDoesNotExist
import json
import logging
import uuid
import html


db = MongoClient("mongo")
collection = db['users']
accounts = collection['accounts']
trips = collection['trips']
#{'username': username, 'tripname': tripname, 'date': date}

# Create your views here.

def view_likes(request: HttpRequest):
    print("\n\n******response******\n\n")
    print(request, flush=True)
    decoded_body = json.loads(request.body.decode())
    tripID = decoded_body["tripID"]
    trip = trips.find_one({"tripID": tripID})
    if trip == None:
        return
    likes = trip.get('likes', [])
    response = {
        "likes": likes
        }
    return JsonResponse(response)

def delete_like(request: HttpRequest):
    token = 'NULL'
    if ('token' in request.COOKIES) :
        token = request.COOKIES['token']
    user = findUser(token)

    username = 'NULL'
    if user != None:
        username = user['username']
    if username == 'NULL': 
        return
    
    decoded_body = json.loads(request.body.decode())
    tripID = decoded_body["tripID"]
    trip = trips.find_one({"tripID": tripID})
    if trip == None:
        return
    
    likes = trip.get('likes', [])
    likes_copy = likes.copy()
    trip_copy = trip.copy()
    if username in likes:
        likes_copy.remove(username)
    trip_copy["likes"] = likes_copy

    # updates = {'$set' : {'likes' : likes}}
    trips.replace_one(trip, trip_copy)

    trip_copy.pop("_id")
    
    response = {
        "likes": likes_copy
    }
    return JsonResponse(response)
    


def add_like(request: HttpRequest):
    token = 'NULL'
    if ('token' in request.COOKIES) :
        token = request.COOKIES['token']
    user = findUser(token)

    username = 'NULL'
    if user != None:
        username = user['username']
    if username == 'NULL': 
        return
    
    decoded_body = json.loads(request.body.decode())
    tripID = decoded_body["tripID"]
    trip = trips.find_one({"tripID": tripID})
    if trip == None:
        return
    
    likes = trip.get('likes', [])
    likes_copy = likes.copy()
    trip_copy = trip.copy()
    if username not in likes:
        likes_copy.append(username)
    trip_copy["likes"] = likes_copy

    # updates = {'$set' : {'likes' : likes}}
    trips.replace_one(trip, trip_copy)

    trip_copy.pop("_id")
    
    response = {
        "likes": likes_copy
    }

    return JsonResponse(response)


def all_trips(request: HttpRequest):
    token = 'NULL'
    if ('token' in request.COOKIES) :
        token = request.COOKIES['token']
    user = findUser(token)

    #If users auth token is not found in the db -> invalid request
    username = 'NULL'
    if user != None:
        username = user['username']
    if username == 'NULL':
        return
    
    trips_cursor = trips.find({})
    trips_list = []
    for trip in trips_cursor:
        trip.pop("_id")
        trips_list.append(trip)
    context = {
        "trips": trips_list,
        "username": username
    }
    print("***** ALL TRIPS *****")
    print(context, flush=True)
    return render(request, "all_trips.html", context)

#TODO: GET USERNAME 
def index_trips(request: HttpRequest):
    # print("\n\n***REQUEST START***\n")
    # print(request)
    # print("\n***REQUEST END***\n\n")
    # print("\n\n***REQUEST BODY START***\n")
    # print(request.body)
    # print("\n\n***REQUEST END***\n\n")

    #Getting the user's auth token
    token = 'NULL'
    if ('token' in request.COOKIES) :
        token = request.COOKIES['token']
    user = findUser(token)

    #If users auth token is not found in the db -> invalid request
    username = 'NULL'
    if user != None:
        username = user['username']
    if username == 'NULL':
        return #RETURN SOMETHING HERE NOT SURE WHAT YET
    
    tripscontext = trips.find({'username': username})
    context = {
        'trips' : tripscontext
    }
    return render(request, 'trips.html', context)

def add_trip(request: HttpRequest):
    # print("\n\n***REQUEST START***\n")
    # print(request)
    # print("\n***REQUEST END***\n\n")
    # print("\n\n***REQUEST BODY START***\n")
    # print(request.body)
    # print("\n\n***REQUEST END***\n\n")
    #Getting the user's auth token
    token = 'NULL'
    if ('token' in request.COOKIES) :
        token = request.COOKIES['token']
    user = findUser(token)

    #If users auth token is not found in the db -> invalid request
    username = 'NULL'
    if user != None:
        username = user['username']
    if username == 'NULL': 
        return #RETURN REDIRECT MAYBE OR SOMETHING NOT SURE 
    decoded_body = json.loads(request.body.decode())
    #print("\n\n **** decoded body start *****\n")
    #print(decoded_body, flush=True)
    #print("\n **** decoded body end *****\n\n", flush=True)

    # rbody = rbody.decode()
    tripname = html.escape(decoded_body["tripName"])
    if tripname == '':
        return
    destination = html.escape(decoded_body["tripDestination"])
    if destination == '':
        return
    trip = {'username': username, 'tripname': tripname, 'destination': destination, 'tripID': str(uuid.uuid1())}
    trips.insert_one(trip)
    
    # tripscontext = trips.find_one({'username': username})
    # l = []
    # for i in tripscontext:
    #     i.pop("_id")
    #     l.append(i)

    trip.pop("_id")
    response = {
        "trips": [trip]
    }

    return JsonResponse(response)

def index(request: HttpRequest):
    context = {
        'logged_out' : True
    }
    if ('token' in request.COOKIES) :
        token = request.COOKIES['token'].encode()
        currToken = hashlib.sha256(token).digest()
        print(currToken)
        entry = accounts.find_one({'token' : currToken})
        if entry != None :
            print('Logging In')
            logged_out = False
            user = entry['username']
            context['username'] = user
            context['logged_out'] = False
            return render(request,"index2.html",context)
    return render(request, "index2.html", context)

def register(request: HttpRequest):
    if request.method == 'POST' :
        print(request)
        body = request.body
        print(body)
        body = body.split(b'&')         #Assuming the body is urlencoded
        username = html.escape(body[1].split(b'=')[1].decode())
        password = html.escape(body[2].split(b'=')[1].decode())
        query = {'username' : username}
        newAcc = accounts.find_one(query)

        if (username == "" or password == "") :
            return invalidRegister()
        
        if (newAcc != None) :
            return invalidRegister()
        
        salt = generateToken(20)
        combined = (password + salt).encode()
        hashed = hashlib.sha256(combined).digest()

        newEntry = {
            'username' : username,
            'password' : hashed,
            'salt' : salt,
            'token' : None
        }
        accounts.insert_one(newEntry)
    
    return HttpResponseRedirect('/')

def login(request: HttpRequest):
    invalid = False
    print("LOGIN")
    if request.method == 'POST' :
        #print(request)
        body = request.body
        body = body.split(b'&')                             #Assuming the body is urlencoded
        username = html.escape(body[1].split(b'=')[1].decode())
        password = html.escape(body[2].split(b'=')[1].decode())
        if username == "" or password == "" :
            return invalidLogin()
        entry = accounts.find_one({'username': username})
        print("Finding User")
        if entry != None :
            print("Found User")
            salt = entry['salt']
            combined = (password + salt).encode()
            attempt = hashlib.sha256(combined).digest()

            if attempt == entry['password']:
                token = generateToken(15)
                hashed = hashlib.sha256(token.encode()).digest()
                updates = {'$set' : {'token' : hashed}}
                accounts.update_one(entry, updates)
                #entry['token'] = hashed
                redirect = HttpResponseRedirect('/')
                print('SUCCESS')
                redirect.set_cookie('token', token, httponly=True)
                redirect.set_cookie('username', username, httponly=True)
                return redirect
            else:
                return invalidLogin()
        else:
            return invalidLogin()

def invalidLogin() :
    #print("Invalid")
    redirect = HttpResponseRedirect('/serveLoginFailed/')
    redirect.context = {'invalid' : True}
    return redirect

def invalidRegister() :
    #print("Invalid")
    redirect = HttpResponseRedirect('/serveRegister/')
    return redirect

def logout (request: HttpRequest) :
    if request.method == 'POST' and 'token' in request.COOKIES:
        user = findUser(request.COOKIES['token'])
        if user != None :
            updates = {'$set' : {'token' : None}}
            accounts.update_one(user, updates)
    redirect = HttpResponseRedirect('/')
    if 'token' in request.COOKIES :
        redirect.delete_cookie('token')
    return redirect

def findUser(token) :
    # REPLACE OR REMOVE
    query = {'token' : hashlib.sha256(token.encode()).digest()}
    account = accounts.find_one(query)
    if account != None :
        return account
    return None

def index2(request: HttpRequest):
    return render(request, "index2.html")

def login2(request: HttpRequest):
    pass


def serveRegister(request: HttpRequest):
    return render(request, "register.html")

def serveLogin(request: HttpRequest):
    return render(request, "login.html")


def serveLoginFailed(request: HttpRequest):
    return render(request, "loginFailed.html")

