from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # default django
    path('register/', view=views.register_with_form_view, name='register'),
    path('login/', view=views.login_view, name='login'),
    path('logout/', view=views.logout_view, name='logout'),

    # social auth
    path('google/', view=views.google_login, name='google_login'),
    path('google/callback/', view=views.google_callback, name='google_callback'),
    path('microsoft/', view=views.microsoft_login, name='microsoft_login'),
    path('microsoft/callback/', view=views.microsoft_callback, name='microsoft_callback'),
]