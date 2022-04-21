import json
from fastapi import APIRouter
from fastapi import FastAPI
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError

router = APIRouter()

# Initialize our OAuth instance from the client ID and client secret specified in our .env file
config = Config('.env')
oauth = OAuth(config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
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
    redirect_uri = request.url_for('auth')

    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.route('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url='/')


@router.get('/logout', tags=['authentication'])  # Tag it as "authentication" for our docs
async def logout(request: Request):
    # Remove the user
    request.session.pop('user', None)

    return RedirectResponse(url='/')