from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'user_profile'

urlpatterns = [
    path('', view=views.index, name='index'),
]
