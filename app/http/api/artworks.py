from fastapi import APIRouter, Depends

from app.http import deps
from app.http.deps import get_db
from app.models.artwork import Artwork
from app.schemas.artwork import ArtworkDetail, ArtworkCreate, ArtworkUpdate

router = APIRouter(
    prefix="/artworks"
)


# 获取所有艺术作品
@router.get("/", response_model=list[ArtworkDetail], dependencies=[Depends(get_db)])
def get_artworks(skip: int = 0):
    """
    获取所有艺术作品列表
    """
    artworks = Artwork.select().offset(skip)
    return list(artworks)


# 根据 ID 获取单个艺术作品信息
@router.get("/{artwork_id}", response_model=ArtworkDetail, dependencies=[Depends(get_db)])
def get_artwork(artwork_id: int):
    """
    根据艺术作品 ID 获取信息
    """
    artwork = Artwork.get_or_none(Artwork.id == artwork_id)
    artwork_detail = ArtworkDetail(
        id=artwork.id,
        artist_id=artwork.artist_id.id,  # 保留 artist_id 字段
        background=artwork.background,
        style=artwork.style,
        theme=artwork.theme,
        artwork=artwork.artwork,
        image=artwork.image
    )
    if not artwork:
        raise HTTPException(status_code=404, detail="艺术作品未找到")
    return artwork_detail


# 根据艺术家 ID 获取所有作品信息
@router.get("/artist/{artist_id}", response_model=list[ArtworkDetail], dependencies=[Depends(get_db)])
def get_artwork(artist_id: int):
    """
    根据艺术家 ID 获取信息
    """
    artworks = Artwork.select().where(Artwork.artist_id == artist_id)
    # 手动构建返回的字典列表
    artwork_details = []
    for artwork in artworks:
        artwork_detail = ArtworkDetail(
            id=artwork.id,
            artist_id=artwork.artist_id.id,  # 保留 artist_id 字段
            background=artwork.background,
            style=artwork.style,
            theme=artwork.theme,
            artwork=artwork.artwork,
            image=artwork.image
        )
        artwork_details.append(artwork_detail)
    if not artwork_details:
        raise HTTPException(status_code=404, detail="艺术作品未找到")
    return list(artwork_details)


# 创建一个新的艺术作品
@router.post("/", response_model=ArtworkDetail, dependencies=[Depends(get_db)])
def create_artwork(request_data: ArtworkCreate):
    """
    创建一个新的艺术作品
    """
    artwork = Artwork.create(
        artist_id=request_data.artist_id,
        artwork=request_data.artwork,
        url=request_data.url,
        background=request_data.background,
        style=request_data.style,
        theme=request_data.theme
    )
    return artwork


# 更新艺术作品信息
@router.put("/{artwork_id}", response_model=ArtworkDetail, dependencies=[Depends(get_db)])
def update_artwork(artwork_id: int, request_data: ArtworkUpdate):
    """
    更新艺术作品信息
    """
    artwork = Artwork.get_or_none(Artwork.id == artwork_id)
    if not artwork:
        raise HTTPException(status_code=404, detail="艺术作品未找到")

    artwork.artwork = request_data.artwork or artwork.artwork
    artwork.url = request_data.url or artwork.url
    artwork.background = request_data.background or artwork.background
    artwork.style = request_data.style or artwork.style
    artwork.theme = request_data.theme or artwork.theme
    artwork.save()
    
    return artwork
