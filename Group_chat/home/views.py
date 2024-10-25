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
        currToken = hashlib.sha256(token).digest()
        entry = userModel.objects.get(token=str(currToken))
        if entry != None :
            print('Logging In')
            logged_out = False
            user = entry.username
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
        username = body[1].split(b'=')[1].decode()
        password = body[2].split(b'=')[1].decode()
        newAcc = userModel.objects.filter(username=username).first()
        if (username == "" or password == "") :
            return invalidRegister()
        
        if (newAcc != None) :
            return invalidRegister()
        
        salt = generateToken(20)
        
        combined = (password + salt).encode()
        hashed = hashlib.sha256(combined).digest()

        # newEntry = {
        #     'username' : username,
        #     'password' : hashed,
        #     'salt' : salt,
        #     'token' : None
        # }
        newEntry = userModel.objects.create(username=username,password=hashed,salt=salt,token="None")
        newEntry.save()
        #accounts.insert_one(newEntry)
    return HttpResponseRedirect('/')

def login(request: HttpRequest):
    invalid = False
    if request.method == 'POST' :
        print(request)
        body = request.body
        body = body.split(b'&')                             #Assuming the body is urlencoded
        username = body[1].split(b'=')[1].decode()
        password = body[2].split(b'=')[1].decode()
        if username == "" or password == "" :
            return wrongPassword()
        entry = userModel.objects.filter(username=username).first()
        print(entry)
        print(username)
        print(password)
        if entry != None :
            salt = entry.salt
            print(salt)
            combined = (password + salt).encode()
            attempt = hashlib.sha256(combined).digest()
            if str(attempt) == entry.password:
                token = generateToken(15)
                hashed = hashlib.sha256(token.encode()).digest()
                entry.token = hashed
                entry.save()
                redirect = HttpResponseRedirect('/')
                print('SUCCESS')
                redirect.set_cookie('token', token)
                return redirect
            else:
                return invalidLogin()
        else:
            return invalidLogin()

def invalidLogin() :
    print("Invalid")
    redirect = HttpResponseRedirect('/serveLogin/')
    redirect.context = {'invalid' : True}
    return redirect

def invalidRegister() :
    print("Invalid")
    redirect = HttpResponseRedirect('/serveRegister')
    return redirect

def logout (request: HttpRequest) :
    if request.method == 'POST' and 'token' in request.COOKIES:
        # REPLACE
        user = findUser(request.COOKIES['token'])
        if user != None :
            user.token = None
    redirect = HttpResponseRedirect('/')
    if 'token' in request.COOKIES :
        redirect.delete_cookie('token')
    return redirect

def findUser(token) :
    # REPLACE OR REMOVE
    account = userModel.objects.get(token=hashlib.sha256(token.encode()).digest())
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

# def register2(request: HttpRequest):
#     if request.method == 'POST' :
#         print(request)
#         body = request.body
#         print(body)
#         body = body.split(b'&')         #Assuming the body is urlencoded
#         username = body[1].split(b'=')[1].decode()
#         password = body[2].split(b'=')[1].decode()
#         salt = generateToken(20)
        
#         combined = (password + salt).encode()
#         hashed = hashlib.sha256(combined).digest()

#         # newEntry = {
#         #     'username' : username,
#         #     'password' : hashed,
#         #     'salt' : salt,
#         #     'token' : None
#         # }
#         newEntry = userModel.objects.create(username=username,password=hashed,salt=salt,token="None")
#         newEntry.save()
#         #accounts.insert_one(newEntry)
#     return HttpResponseRedirect('/index2/')

# def login2(request: HttpRequest):
#     return return HttpResponseRedirect('/index2/')
# class AllTrips(ListView):
#     model = TripItem
#     template_name = "trips.html"

