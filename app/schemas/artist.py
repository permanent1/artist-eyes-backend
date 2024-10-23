from typing import List, Optional
from pydantic import BaseModel

# Shared properties
class ArtistBase(BaseModel):
    id: int
    name: str
    year: str
    genre: str
    image: str

    class Config:
        orm_mode = True


class ArtistDetail(ArtistBase):
    introduction: Optional[str] = None
    background: Optional[str] = None
    style: Optional[str] = None
    characters: Optional[str] = None
    website: Optional[str] = None


class ArtistCreate(BaseModel):
    name: str
    year: Optional[str] = None
    genre: Optional[str] = None
    introduction: Optional[str] = None
    background: Optional[str] = None
    style: Optional[str] = None
    characters: Optional[str] = None
    website: Optional[str] = None


class ArtistUpdate(BaseModel):
    name: Optional[str]
    year: Optional[str]
    genre: Optional[str]
    introduction: Optional[str]
    background: Optional[str]
    style: Optional[str]
    characters: Optional[str]
    website: Optional[str]
