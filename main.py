import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.engine import create_engine
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse

from app.internal import admin
from app.dependencies import get_query_token, get_token_header
from app.routers import users
import app.sql.database as db

app = FastAPI(docs_url="/docs", redoc_url="/redoc")

# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )

@app.on_event("startup")
async def startup() -> None:
    SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URI')
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    db.Base.metadata.create_all(bind=engine)


@app.on_event("shutdown")
async def shutdown():
    db.SessionLocal().close()
    
app.include_router(users.router)

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(SessionMiddleware, secret_key='!secret')
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


