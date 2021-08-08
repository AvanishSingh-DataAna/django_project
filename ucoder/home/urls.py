from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('search', views.search, name='search'),
    path('signup', views.handelSignup, name='handelSignup'),
    path('login', views.handelLogin, name='handelLogin'),
    path('logout', views.handelLogout, name='handelLogout'),

]