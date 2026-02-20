from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'authentication'

urlpatterns = [
    # default django
    path('register/', view=views.register_view, name='register'),
    path('register-with-form/', view=views.register_with_form_view, name='register_with_form'),
    path('login/', view=views.login_view, name='login'),
    path('logout/', view=views.logout_view, name='logout'),

    # social auth
    path('google/', view=views.google_login, name='google_login'),
    path('google/callback/', view=views.google_callback, name='google_callback'),
]