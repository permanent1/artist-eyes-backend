from typing import Optional
from pydantic import BaseModel
from app.schemas.artist import ArtistDetail

# Shared properties
class ArtworkBase(BaseModel):
    id: int
    artwork: str
    image: str

    class Config:
        orm_mode = True


class ArtworkDetail(ArtworkBase):
    artist_id: int
    background: Optional[str] = None
    style: Optional[str] = None
    theme: Optional[str] = None


class ArtworkDetail_m(ArtworkBase):
    artist_id: ArtistDetail
    background: Optional[str] = None
    style: Optional[str] = None
    theme: Optional[str] = None


class ArtworkCreate(BaseModel):
    artist_id: int
    artwork: str
    image: str
    background: Optional[str] = None
    style: Optional[str] = None
    theme: Optional[str] = None


class ArtworkUpdate(BaseModel):
    artwork: Optional[str]
    image: Optional[str]
    background: Optional[str]
    style: Optional[str]
    theme: Optional[str]
