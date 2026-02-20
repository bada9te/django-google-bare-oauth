from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm

from .utils.google_oauth import *
from .utils.microsoft_oauth import *


# Create your views here.
def login_view(request):
    if request.user and request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect(reverse('user_profile:index'))
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in successfully.')
            return redirect(reverse('user_profile:index'))
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
            return render(request, 'login.html')
    
    context = {}
    return render(request, 'login.html', context)


# def register_view(request):
#     if request.user and request.user.is_authenticated:
#         messages.info(request, 'You are already logged in.')
#         return redirect(reverse('user_profile:index'))
    
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password1 = request.POST.get('password1')
#         password2 = request.POST.get('password2')

#         if not email or not password1 or not password2:
#             messages.error(request, 'All fields are required. Please fill in all fields.')
#             return render(request, 'user_profile/register.html')
        
#         if password1 != password2:
#             messages.error(request, 'Passwords do not match. Please try again.')
#             return render(request, 'user_profile/register.html')
        
#         if User.objects.filter(username=email).exists():
#             messages.error(request, 'Email is already registered. Please use a different email.')
#             return render(request, 'user_profile/register.html')
        
#         user = User.objects.create_user(
#             username=email, 
#             email=email, 
#             password=password1
#         )
#         user.save()
        
#         login(request, user)
#         messages.success(request, 'You have been registered and logged in successfully.')
#         return redirect(reverse('user_profile:index'))

#     context = {}
#     return render(request, 'user_profile/register.html', context)


def register_with_form_view(request):
    if request.user and request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect(reverse('user_profile:index'))
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            target_email = form.cleaned_data['username']
            print("TARGET_EMAIL:", target_email)
            
            if User.objects.filter(username=target_email).exists():
                messages.error(request, 'Email is already registered. Please use a different email.')
                return render(request, 'register_with_form.html', {'form': form})

            user.email = target_email
            user.save()
            login(request, user)
            messages.success(request, 'You have been registered and logged in successfully.')
            return redirect(reverse('user_profile:index'))
        else:        
            return render(request, 'register_with_form.html', {'form': form})
    
    form = CustomUserCreationForm()
    context = {
        "form": form
    }
    return render(request, 'register_with_form.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect(reverse('user_profile:index'))


def google_login(request):
    if request.user and request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect(reverse('user_profile:index'))
    
    target = google_oauth_get_login_screen_url(request)
    return redirect(target)


def google_callback(request):
    code = request.GET.get('code')
    
    if not code:
        messages.error(request, 'Authorization failed.')
        return redirect(reverse('authentication:login'))
    
    # exchange code for access token
    
    access_token = google_oauth_get_access_token(code, request)
    # print("GOOGLE ACCESS_TOKEN:", access_token)
    
    # get user info
    user_data = google_oauth_get_user_info_json(access_token)
    print("GOOGLE USER_DATA:", user_data)
    
    email = user_data.get('email')
    # name = user_data.get('name')

    user = User.objects.filter(username=email).first()
    
    if not user:
        user = User.objects.create_user(
            username=email, 
            email=email,
            first_name=user_data.get('given_name', ''),
            last_name=user_data.get('family_name', ''), 
        )
        user.save()

    login(request, user)
    
    return redirect(reverse('user_profile:index'))



def microsoft_login(request):
    if request.user and request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect(reverse('user_profile:index'))
    
    # Build the Microsoft authorization URL
    target = microsoft_oauth_get_login_screen_url(request)
    return redirect(target)


def microsoft_callback(request):
    code = request.GET.get('code')
    
    if not code:
        messages.error(request, 'Authorization failed.')
        return redirect(reverse('authentication:login'))
    
    # Exchange code for access token
    access_token = microsoft_oauth_get_access_token(code, request)
    # print("MICROSOFT ACCESS_TOKEN:", access_token)
    
    # Get user info
    user_data = microsoft_oauth_get_user_info_json(access_token)
    print("MICROSOFT USER_DATA:", user_data)
    
    email = user_data.get('mail') or user_data.get('userPrincipalName')

    user = User.objects.filter(username=email).first()
    
    if not user:
        user = User.objects.create_user(
            username=email, 
            email=email,
            first_name=user_data.get('givenName', ''),
            last_name=user_data.get('surname', ''), 
        )
        user.save()

    login(request, user)
    
    return redirect(reverse('user_profile:index'))
