from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from .views import home, login, register, update,logout
urlpatterns = [
    path('',home,name="home"),
    path('login',login,name="login"),
    path('register',register,name="register"),
    path("logout",logout,name='logout'),
    path('update/<int:pk>',update,name="update")    
]
