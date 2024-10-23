from fastapi import APIRouter, Depends, HTTPException
from peewee import DoesNotExist, prefetch

from app.http import deps
from app.http.deps import get_db
from app.models.artist import Artist
from app.models.artwork import Artwork
from app.models.phase import Phase
from app.schemas.artist import ArtistDetail, ArtistCreate, ArtistUpdate
from app.schemas.artwork import ArtworkDetail, ArtworkCreate, ArtworkUpdate
from app.schemas.phase import PhaseDetail, PhaseCreate, PhaseUpdate

router = APIRouter(
    prefix="/artists"
)


# 获取所有艺术家
@router.get("/", response_model=list[ArtistDetail], dependencies=[Depends(get_db)])
def get_artists(skip: int = 0):
    """
    获取所有艺术家详细信息列表，包含artworks和phases
    """
    # 查询艺术家
    artists = Artist.select().offset(skip)

    return list(artists)


# 根据 ID 获取单个艺术家信息
@router.get("/{artist_id}", response_model=ArtistDetail, dependencies=[Depends(get_db)])
def get_artist(artist_id: int):
    """
    根据艺术家 ID 获取艺术家信息
    """
    try:
        artist = Artist.get_by_id(artist_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="艺术家未找到")
    return artist


# 创建艺术家
@router.post("/", response_model=ArtistDetail, dependencies=[Depends(get_db)])
def create_artist(request_data: ArtistCreate):
    """
    创建一个新艺术家
    """
    artist = Artist.create(
        name=request_data.name,
        year=request_data.year,
        genre=request_data.genre,
        introduction=request_data.introduction,
        background=request_data.background,
        style=request_data.style,
        characters=request_data.characters,
        website=request_data.website
    )
    return artist


# 更新艺术家
@router.put("/{artist_id}", response_model=ArtistDetail, dependencies=[Depends(get_db)])
def update_artist(artist_id: int, request_data: ArtistUpdate):
    """
    更新艺术家信息
    """
    artist = Artist.get_or_none(Artist.id == artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="艺术家未找到")

    artist.name = request_data.name or artist.name
    artist.year = request_data.year or artist.year
    artist.genre = request_data.genre or artist.genre
    artist.introduction = request_data.introduction or artist.introduction
    artist.background = request_data.background or artist.background
    artist.style = request_data.style or artist.style
    artist.characters = request_data.characters or artist.characters
    artist.website = request_data.website or artist.website

    artist.save()
    return artist


# 删除艺术家
@router.delete("/{artist_id}", dependencies=[Depends(get_db)])
def delete_artist(artist_id: int):
    """
    删除艺术家
    """
    artist = Artist.get_or_none(Artist.id == artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="艺术家未找到")
    
    artist.delete_instance()
    return {"detail": "艺术家已删除"}
