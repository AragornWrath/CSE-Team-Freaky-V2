import json
from channels.generic.websocket import AsyncWebsocketConsumer
import hashlib
from pymongo import MongoClient

db = MongoClient("mongo")
collection = db['users']
accounts = collection['accounts']
trips = collection['trips']
class LikeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        auth_token = find_auth_token(self.scope["headers"])
        print("auth token found: ", auth_token, flush=True)
        user = findUser(auth_token)
        username = 'NULL'
        if user != None:
            username = user['username']
        print("username: ", username, flush=True)
        await self.accept()

        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'you are now connected! :)',
            
        }))

    async def receive(self, text_data):
        like_data_json = json.loads(text_data)
        print("like data: ", like_data_json, flush=True)
#Make sure if you want to print something you use flush=True

def find_auth_token(headers):
    #call with the headers from self.scope["headers"]
    for header_tuple in headers:
            if b'cookie' in header_tuple:
                cookies = header_tuple[1]
                string_cookies = cookies.decode()
                cookie_list = string_cookies.split()
                for cookie in cookie_list:
                    if cookie.startswith('token='):
                        cookie = cookie.replace(';', '')
                        token_split = cookie.split('=', 1)
                        token = token_split[1]
                        #print("token: ", token, flush=True)
                        return token
    return 'no_auth_token'

def model_add_likes():
    token = 'NULL'
    if ('token' in request.COOKIES) :
        token = request.COOKIES['token']
    user = findUser(token)

    username = 'NULL'
    if user != None:
        username = user['username']
    if username == 'NULL': 
        return HttpResponseForbidden()
    
    decoded_body = json.loads(request.body.decode())
    tripID = decoded_body["tripID"]
    trip = trips.find_one({"tripID": tripID})
    if trip == None:
        return HttpResponseForbidden()
    
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


def findUser(token) :
    # REPLACE OR REMOVE
    query = {'token' : hashlib.sha256(token.encode()).digest()}
    account = accounts.find_one(query)
    if account != None :
        return account
    return None