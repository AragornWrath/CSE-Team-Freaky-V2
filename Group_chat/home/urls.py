from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('serveRegister/register/', views.register, name='register'),
    path('serveLogin/login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path("trips/", views.index_trips, name="trips"),
    #path('index2/', views.index2, name='index2'),
    path('serveRegister/', views.serveRegister, name='serverRegister'),
    path('serveLogin/', views.serveLogin, name='serveLogin'),
    #path('serveRegister2/register2/', views.register2, name='register2'),
]
