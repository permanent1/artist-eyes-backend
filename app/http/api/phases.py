from fastapi import APIRouter, Depends, HTTPException

from app.http import deps
from app.http.deps import get_db
from app.models.phase import Phase
from app.schemas.phase import PhaseDetail, PhaseCreate, PhaseUpdate

router = APIRouter(
    prefix="/phases"
)


# 获取所有阶段
@router.get("/", response_model=list[PhaseDetail], dependencies=[Depends(get_db)])
def get_phases(skip: int = 0, limit: int = 10):
    """
    获取所有阶段列表
    """
    phases = Phase.select().offset(skip).limit(limit)
    # 手动构建返回的字典列表
    phase_details = []
    for phase in phases:
        phase_detail = PhaseDetail(
            id=phase.id,
            artist_id=phase.artist_id.id,  # 保留 artist_id 字段
            phase=phase.phase,
            name=phase.name,
            introduction=phase.introduction,
            background=phase.background,
            style=phase.style,
            theme=phase.theme,
            meaning=phase.meaning,
            artwork=phase.artwork,
            image=phase.image
        )
        phase_details.append(phase_detail)
    if not phase_details:
        raise HTTPException(status_code=404, detail="阶段未找到")
    return list(phase_details)


# 根据 ID 获取单个阶段
@router.get("/{phase_id}", response_model=PhaseDetail, dependencies=[Depends(get_db)])
def get_phase(phase_id: int):
    """
    根据阶段 ID 获取信息
    """
    phase = Phase.get_or_none(Phase.id == phase_id)
    phase_detail = PhaseDetail(
        id=phase.id,
        artist_id=phase.artist_id.id,  # 保留 artist_id 字段
        phase=phase.phase,
        name=phase.name,
        introduction=phase.introduction,
        background=phase.background,
        style=phase.style,
        theme=phase.theme,
        meaning=phase.meaning,
        artwork=phase.artwork,
        image=phase.image
    )
    if not phase:
        raise HTTPException(status_code=404, detail="阶段未找到")
    return phase_detail


# 根据艺术家 ID 获取所有阶段
@router.get("/artist/{artist_id}", response_model=list[PhaseDetail], dependencies=[Depends(get_db)])
def get_phase(artist_id: int):
    """
    根据艺术家 ID 获取信息
    """
    phases = Phase.select().where(Phase.artist_id == artist_id)
    # 手动构建返回的字典列表
    phase_details = []
    for phase in phases:
        phase_detail = PhaseDetail(
            id=phase.id,
            artist_id=phase.artist_id.id,  # 保留 artist_id 字段
            phase=phase.phase,
            name=phase.name,
            introduction=phase.introduction,
            background=phase.background,
            style=phase.style,
            theme=phase.theme,
            meaning=phase.meaning,
            artwork=phase.artwork,
            image=phase.image
        )
        phase_details.append(phase_detail)
    if not phase_details:
        raise HTTPException(status_code=404, detail="阶段未找到")
    return list(phase_details)


# 创建新阶段
@router.post("/", response_model=PhaseDetail, dependencies=[Depends(get_db)])
def create_phase(request_data: PhaseCreate):
    """
    创建一个新的阶段
    """
    phase = Phase.create(
        artist_id=request_data.artist_id,
        phase=request_data.phase,
        name=request_data.name,
        introduction=request_data.introduction,
        background=request_data.background,
        style=request_data.style,
        theme=request_data.theme,
        meaning=request_data.meaning,
        artwork=request_data.artwork,
        image=request_data.image
    )
    return phase


# 更新阶段
@router.put("/{phase_id}", response_model=PhaseDetail, dependencies=[Depends(get_db)])
def update_phase(phase_id: int, request_data: PhaseUpdate):
    """
    更新阶段信息
    """
    phase = Phase.get_or_none(Phase.id == phase_id)
    if not phase:
        raise HTTPException(status_code=404, detail="阶段未找到")

    phase.phase = request_data.phase or phase.phase
    phase.name = request_data.name or phase.name
    phase.introduction = request_data.introduction or phase.introduction
    phase.background = request_data.background or phase.background
    phase.style = request_data.style or phase.style
    phase.theme = request_data.theme or phase.theme
    phase.meaning = request_data.meaning or phase.meaning
    phase.artwork = request_data.artwork or phase.artwork
    phase.image = request_data.image or phase.image
    phase.save()
    
    return phase


# 删除阶段
@router.delete("/{phase_id}", response_model=dict, dependencies=[Depends(get_db)])
def delete_phase(phase_id: int):
    """
    删除阶段
    """
    phase = Phase.get_or_none(Phase.id == phase_id)
    if not phase:
        raise HTTPException(status_code=404, detail="阶段未找到")

    phase.delete_instance()
    return {"msg": "阶段已删除"}
