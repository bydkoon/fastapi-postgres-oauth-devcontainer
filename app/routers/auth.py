import os
import requests
from dataclasses import dataclass
from http import HTTPStatus
from fastapi import Security, APIRouter, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer, SecurityScopes
from starlette.requests import Request
from starlette.config import Config
from starlette.responses import RedirectResponse, JSONResponse
from authlib.integrations.starlette_client import OAuth, OAuthError

AUTHORIZATION_URL = os.environ.get(
    "AUTHORIZATION_URL", "https://accounts.google.com/o/oauth2/auth"
)
TOKEN_URL = os.environ.get("TOKEN_URL", "https://oauth2.googleapis.com/token")

JWKS_URI = os.environ.get(
    "JWKS_URI", "https://www.googleapis.com/oauth2/v3/certs"
)

ALGORITHMS = ["RS256"]

USER_INFO_URL = (
    "https://www.googleapis.com/oauth2/v2/userinfo?access_token={access_token}"
)

TOKEN_INFO_URL = (
    "https://oauth2.googleapis.com/tokeninfo?access_token={access_token}"
)

router = APIRouter(
    tags=["authentication"],
    responses={404: {"description": "Not found"}},
)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

# Initialize our OAuth instance from the client ID and client secret specified in our .env file
config = Config('.env')
oauth = OAuth(config)

oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@router.get('/login', tags=['authentication'])  # Tag it as "authentication" for our docs
async def login(request: Request):
    # Redirect Google OAuth back to our application
    # redirect_uri = request.url_for('auth')
    redirect_uri = 'http://localhost:8000/auth'

    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get('/logout', tags=['authentication'])  # Tag it as "authentication" for our docs
async def logout(request: Request):
    # Remove the user
    request.session.pop('user', None)

    return RedirectResponse(url='/')

@router.get('/auth')
async def auth(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
        print(access_token)
    except OAuthError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    user_data = await oauth.google.parse_id_token(request, access_token)
    # TODO: validate email in our database and generate JWT token
    jwt = f'valid-jwt-token-for-{user_data["email"]}'
    # TODO: return the JWT token to the user so it can make requests to our /api endpoint
    return JSONResponse({'result': True, 'access_token': jwt})

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@dataclass
class GoogleIDToken:
    azp: str = ""
    aud: str = ""
    sub: str = ""
    scope: str = ""
    exp: str = ""
    expires_in: str = ""
    email: str = ""
    email_verified: str = ""
    access_type: str = ""


# Define a Authorization scheme specific to our Auth0 config
auth0_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=AUTHORIZATION_URL,
    tokenUrl=TOKEN_URL,
    scopes={"openid": "openid", "email": "email", "profile": "profile"},
)



async def get_current_user(
    security_scopes: SecurityScopes, token: str = Security(auth0_scheme)
):
    if not verify(token):
        raise AuthError(
            error="유효하지 않은 토큰입니다", status_code=HTTPStatus.UNAUTHORIZED
        )
    response = requests.get(USER_INFO_URL.format(access_token=token))
    if response.status_code == HTTPStatus.OK:
        return response.json()


def verify(token: str) -> bool:
    response = requests.get(TOKEN_INFO_URL.format(access_token=token))
    google_id_token: GoogleIDToken = (
        GoogleIDToken(**response.json())
        if response.status_code == HTTPStatus.OK
        else GoogleIDToken(expires_in="0")
    )
    return int(google_id_token.expires_in) > 0