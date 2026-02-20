import requests
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .env import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from .forms import CustomUserCreationForm


def build_google_redirect_uri(request):
    scheme = 'https' if request.is_secure() else 'http'
    host = request.get_host()
    return f"{scheme}://{host}{GOOGLE_REDIRECT_URI_PARTIAL}"


# Contants for Google OAuth
GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'
GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_REDIRECT_URI_PARTIAL = '/auth/google/callback'
GOOGLE_SCOPE = ' '.join([
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
])


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
            return render(request, 'user_profile/login.html')
    
    context = {}
    return render(request, 'user_profile/login.html', context)


def register_view(request):
    if request.user and request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect(reverse('user_profile:index'))
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not email or not password1 or not password2:
            messages.error(request, 'All fields are required. Please fill in all fields.')
            return render(request, 'user_profile/register.html')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, 'user_profile/register.html')
        
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email is already registered. Please use a different email.')
            return render(request, 'user_profile/register.html')
        
        user = User.objects.create_user(
            username=email, 
            email=email, 
            password=password1
        )
        user.save()
        
        login(request, user)
        messages.success(request, 'You have been registered and logged in successfully.')
        return redirect(reverse('user_profile:index'))

    context = {}
    return render(request, 'user_profile/register.html', context)


def register_with_form_view(request):
    if request.user and request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect(reverse('user_profile:index'))
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)

                target_email = form.cleaned_data['email']
                print("TARGET_EMAIL:", target_email)
                
                if User.objects.filter(username=user.email).exists():
                    messages.error(request, 'Email is already registered. Please use a different email.')
                    return render(request, 'user_profile/register_with_form.html', {'form': form})

                user.username = target_email
                user.save()
                login(request, user)
                messages.success(request, 'You have been registered and logged in successfully.')
                return redirect(reverse('user_profile:index'))
            except:
                messages.error(request, f'An error occurred during registration')
    
    form = CustomUserCreationForm()
    context = {
        "form": form
    }
    return render(request, 'user_profile/register_with_form.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect(reverse('user_profile:index'))


def google_login(request):
    if request.user and request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect(reverse('user_profile:index'))
    
    target = f"{GOOGLE_AUTH_URL}?client_id={GOOGLE_CLIENT_ID}&redirect_uri={build_google_redirect_uri(request)}&response_type=code&scope={GOOGLE_SCOPE}&access_type=offline&prompt=consent"
    return redirect(target)


def google_callback(request):
    code = request.GET.get('code')
    
    if not code:
        messages.error(request, 'Authorization failed.')
        return redirect(reverse('authentication:login'))
    
    # exchange code for access token
    token_data = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': build_google_redirect_uri(request),
        'grant_type': 'authorization_code',
    }
    
    token_response = requests.post(GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=token_data)
    access_token = token_response.json().get('access_token')

    print("ACCESS_TOKEN:", access_token)
    
    # get user info
    user_info_response = requests.get(
        GOOGLE_USER_INFO_URL,
        headers={'Authorization': f'Bearer {access_token}'}
    )
    user_data = user_info_response.json()

    print("USER_DATA:", user_data)
    
    email = user_data.get('email')
    # name = user_data.get('name')

    user = User.objects.filter(username=email).first()
    
    if not user:
        user = User.objects.create_user(
            username=email, 
            email=email, 
        )
        user.save()

    login(request, user)
    
    return redirect(reverse('user_profile:index'))
