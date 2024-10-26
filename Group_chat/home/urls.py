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
]
