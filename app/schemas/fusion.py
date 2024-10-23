from typing import Optional
from datetime import datetime
from pydantic import BaseModel, validator
from app.support.helper import format_datetime

from app.schemas.artist import ArtistDetail
from app.schemas.user import UserDetail

# Shared properties
class FusionBase(BaseModel):
    id: int
    draft: str
    title: Optional[str] = None
    fusion: Optional[str] = None

    class Config:
        orm_mode = True


class FusionDetail(FusionBase):
    user_id: int
    artist_id: int
    description: Optional[str] = None
    updated_at: datetime


class FusionDetail_m(FusionBase):
    user_id: UserDetail
    artist_id: ArtistDetail
    description: Optional[str] = None
    updated_at: datetime


class FusionCreate(BaseModel):
    user_id: int
    phase_id: int
    draft: str


class FusionUpdate(BaseModel):
    fusion: str
    title: str
    description: str
