import requests
from ..env import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET


# Contants for Google OAuth
GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'
GOOGLE_SCOPE = ' '.join([
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
])


def google_oauth_build_redirect_uri(request):
    scheme = 'https' if request.is_secure() else 'http'
    host = request.get_host()
    return f"{scheme}://{host}/auth/google/callback"


def google_oauth_get_login_screen_url(request):
    return f"{GOOGLE_AUTH_URL}?client_id={GOOGLE_CLIENT_ID}&redirect_uri={google_oauth_build_redirect_uri(request)}&response_type=code&scope={GOOGLE_SCOPE}&access_type=offline&prompt=consent"


def google_oauth_get_access_token(code, request):
    # Exchange code for access token
    token_data = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': google_oauth_build_redirect_uri(request),
        'grant_type': 'authorization_code',
    }
    
    token_response = requests.post(GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=token_data)
    return token_response.json().get('access_token')


def google_oauth_get_user_info_json(access_token):
    user_info_response = requests.get(
        GOOGLE_USER_INFO_URL,
        headers={'Authorization': f'Bearer {access_token}'}
    )
    return user_info_response.json()