import requests
from ..env import MICROSOFT_CLIENT_ID, MICROSOFT_CLIENT_SECRET


# Constants for Microsoft OAuth
MICROSOFT_AUTH_URL = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
MICSOFT_ACCESS_TOKEN_OBTAIN_URL = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
MICROSOFT_USER_INFO_URL = 'https://graph.microsoft.com/v1.0/me'
MICROSOFT_SCOPE = 'User.Read'


def microsoft_oauth_build_redirect_uri(request):
    scheme = 'https' if request.is_secure() else 'http'
    host = request.get_host()
    return f"{scheme}://{host}/auth/microsoft/callback"


def microsoft_oauth_get_login_screen_url(request):
    return f"{MICROSOFT_AUTH_URL}?client_id={MICROSOFT_CLIENT_ID}&response_type=code&redirect_uri={microsoft_oauth_build_redirect_uri(request)}&scope={MICROSOFT_SCOPE}"


def microsoft_oauth_get_access_token(code, request):
    # Exchange code for access token
    token_data = {
        'code': code,
        'client_id': MICROSOFT_CLIENT_ID,
        'client_secret': MICROSOFT_CLIENT_SECRET,
        'redirect_uri': microsoft_oauth_build_redirect_uri(request),
        'grant_type': 'authorization_code',
    }
    
    token_response = requests.post(MICSOFT_ACCESS_TOKEN_OBTAIN_URL, data=token_data)
    return token_response.json().get('access_token')


def microsoft_oauth_get_user_info_json(access_token):
    user_info_response = requests.get(
        MICROSOFT_USER_INFO_URL,
        headers={'Authorization': f'Bearer {access_token}'}
    )
    return user_info_response.json()

