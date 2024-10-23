from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, HttpResponseNotFound
from django.template import loader, RequestContext
# from pymongo import MongoClient
from bcrypt import hashpw, gensalt
from home.generateToken import generateToken
import hashlib
from .models import userModel

from django.views.generic import ListView
from .models import TripItem

db = MongoClient("mongo")
collection = db['users']
accounts = collection['accounts']

# Create your views here.
def index_trips(request: HttpRequest):
    trips = TripItem.objects.all()  # Fetch all task objects
    return render(request, 'trips.html', {'object_list': trips})

def index(request: HttpRequest):
    context = {
        'logged_out' : True
    }
    if ('token' in request.COOKIES) :
        token = request.COOKIES['token'].encode()
        query = {'token' : hashlib.sha256(token).digest()}
        result = accounts.find_one(query)
        if result != None :
            print('Logging In')
            logged_out = False
            user = result['username']
            context['username'] = user
            context['logged_out'] = False
            return render(request,"index.html",context)
    return render(request, "index.html", context)

def register(request: HttpRequest):
    if request.method == 'POST' :
        print(request)
        body = request.body
        print(body)
        body = body.split(b'&')         #Assuming the body is urlencoded
        username = body[1].split(b'=')[1].decode()
        password = body[2].split(b'=')[1]
        salt = gensalt()
        hashed = hashpw(password,salt)

        # newEntry = {
        #     'username' : username,
        #     'password' : hashed,
        #     'salt' : salt,
        #     'token' : None
        # }
        newEntry = userModel.objects.create(username=username,password=hashed,salt=salt,token="None")
        newEntry.save()
        #accounts.insert_one(newEntry)
    return HttpResponseRedirect('/home')

def login(request: HttpRequest):
    if request.method == 'POST' :
        print(request)
        body = request.body
        body = body.split(b'&')         #Assuming the body is urlencoded
        username = body[1].split(b'=')[1].decode()
        password = body[2].split(b'=')[1]
        query = {'username' : username}
        result = accounts.find_one(query)

        # REPLACE 
        if result != None :
            salt = result['salt']
            attempt = hashpw(password,salt)
            if attempt == result['password'] :
                token = generateToken()
                hashed = hashlib.sha256(token.encode()).digest()
                updates = {'$set': {'token' : hashed}}
                accounts.update_one(result,updates)
        # REPLACE
                redirect = HttpResponseRedirect('/home')
                redirect.set_cookie('token', token)
                return redirect
        else :
            return HttpResponseNotFound()    #Replace this with a redirect at one point.


def logout (request: HttpRequest) :
    if request.method == 'POST' and 'token' in request.COOKIES:
        # REPLACE
        user = findUser(request.COOKIES['token'])
        if user != None :
            user['token'] = None
    redirect = HttpResponseRedirect('/home')
    if 'token' in request.COOKIES :
        redirect.delete_cookie('token')
    return redirect

def findUser(token) :
    # REPLACE OR REMOVE
    account = accounts.find_one({'token' : hashlib.sha256(token.encode()).digest()})
    if account != None :
        return account
    return None

class AllTrips(ListView):
    model = TripItem
    template_name = "trips.html"

