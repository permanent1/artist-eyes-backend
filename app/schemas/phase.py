from typing import Optional
from pydantic import BaseModel
from app.schemas.artist import ArtistDetail

# Shared properties
class PhaseBase(BaseModel):
    id: int
    phase: str
    name: str
    image: str

    class Config:
        orm_mode = True


class PhaseDetail(PhaseBase):
    artist_id: int
    introduction: Optional[str] = None
    background: Optional[str] = None
    style: Optional[str] = None
    theme: Optional[str] = None
    meaning: Optional[str] = None
    artwork: Optional[str] = None


class PhaseDetail_m(PhaseBase):
    artist_id: ArtistDetail
    introduction: Optional[str] = None
    background: Optional[str] = None
    style: Optional[str] = None
    theme: Optional[str] = None
    meaning: Optional[str] = None
    artwork: Optional[str] = None


class PhaseCreate(BaseModel):
    artist_id: int
    phase: str
    name: str
    image: str
    introduction: Optional[str] = None
    background: Optional[str] = None
    style: Optional[str] = None
    theme: Optional[str] = None
    meaning: Optional[str] = None
    artwork: Optional[str] = None


class PhaseUpdate(BaseModel):
    phase: Optional[str]
    name: Optional[str]
    image: Optional[str]
    introduction: Optional[str]
    background: Optional[str]
    style: Optional[str]
    theme: Optional[str]
    meaning: Optional[str]
    artwork: Optional[str]
