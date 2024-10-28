from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path("trips/", views.index_trips, name="trips"),
    path('serveRegister/', views.serveRegister, name='serverRegister'),
    path('serveLogin/', views.serveLogin, name='serveLogin'),
    path('serveLoginFailed/', views.serveLoginFailed, name='serveLogin'),
    path('serveLoginFailed/login/', views.login, name='login'),
    path('trips/add-trip/', views.add_trip, name='addTrip'),
    path('all_trips/', views.all_trips, name='allTrips'),
    path('all_trips/add-like', views.add_like, name="addLike"),
    #path('all_trips/delete-like', views.delete_like, name="deleteLike"),
]
