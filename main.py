from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.config import Config
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse

from authlib.integrations.starlette_client import OAuth

from router import auth(

app = FastAPI()
app.mount('/auth', auth)
app.mount('/api', api_app)

app = FastAPI(docs_url=None, redoc_url=None)
app.add_middleware(SessionMiddleware, secret_key='!secret')
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(auth, prefix="/auth")