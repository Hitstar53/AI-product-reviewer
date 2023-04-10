from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('payment/', views.payment, name='payment'),
    path('payment/success/', views.success, name='success'),
    path('contact/', views.contact, name='contact'),
    path('history/', views.history, name='history'),
    path('search/', views.search, name='search'),
]