from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from httpx import main
from starlette.config import Config
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth
import uvicorn
from routers import auth

app = FastAPI()
app.mount('/auth', auth)

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

@app.get('/login', tags=['authentication'])  # Tag it as "authentication" for our docs
async def login(request: Request):
    # Redirect Google OAuth back to our application
    redirect_uri = request.url_for('auth')

    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get('/logout', tags=['authentication'])  # Tag it as "authentication" for our docs
async def logout(request: Request):
    # Remove the user

    request.session.pop('user', None)

    return RedirectResponse(url='/')

@app.get('/')
async def home(request: Request):
    user = request.session.get('user')

    if user is not None:
        email = user['email']
        html = (
            f'<pre>Email: {email}</pre><br>'
            '<a href="/docs">documentation</a><br>'
            '<a href="/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/login">login</a>')

# app.include_router(auth, prefix="/auth")
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0"
                , port=5000, reload=True
                )