from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse

from main import app, oauth


@app.route('/auth')
async def auth(request: Request):
    # Perform Google OAuth
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)

    # Save the user
    request.session['user'] = dict(user)

    return RedirectResponse(url='/')



# Try to get the logged in user
async def get_user(request: Request) -> Optional[dict]:
    user = request.session.get('user')
    if user is not None:
        return user
    else:
        raise HTTPException(status_code=403, detail='Could not validate credentials.')

    return None
