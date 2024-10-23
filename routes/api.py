from fastapi import APIRouter
from app.http.api import demo
from app.http.api import auth
from app.http.api import users
from app.http.api import artists
from app.http.api import artworks
from app.http.api import fusions
from app.http.api import phases

api_router = APIRouter()

api_router.include_router(demo.router, tags=["demo"])

api_router.include_router(auth.router, tags=["auth"])

api_router.include_router(users.router, tags=["users"])

api_router.include_router(artists.router, tags=["artists"])

api_router.include_router(artworks.router, tags=["artworks"])

api_router.include_router(fusions.router, tags=["fusions"])

api_router.include_router(phases.router, tags=["phases"])
