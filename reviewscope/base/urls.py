from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('payment/<str:plan>/', views.payment, name='payment'),
    path('success/', views.success, name='success'),
    path('contact/', views.contact, name='contact'),
    path('reviews/', views.reviews, name='reviews'),
    path('search/', views.search, name='search'),
]