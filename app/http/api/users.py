from fastapi import APIRouter, Depends

from app.http import deps
from app.http.deps import get_db
from app.models.user import User
from app.schemas.user import UserDetail,UserCreate,UserUpdate
from app.services.auth import hashing

router = APIRouter(
    prefix="/users"
)


@router.get("/me", response_model=UserDetail, dependencies=[Depends(get_db)])
def me(auth_user: User = Depends(deps.get_auth_user)):
    """
    当前登录用户信息
    """
    return auth_user


# 获取所有用户
@router.get("/", response_model=list[UserDetail], dependencies=[Depends(get_db)])
def get_users(skip: int = 0, limit: int = 10):
    """
    获取所有用户列表
    """
    users = User.select().offset(skip).limit(limit)
    return list(users)


# 根据 ID 获取单个用户信息
@router.get("/{user_id}", response_model=UserDetail, dependencies=[Depends(get_db)])
def get_user(user_id: int):
    """
    根据用户 ID 获取用户信息
    """
    user = User.get_or_none(User.id == user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")
    return user


# 更新用户信息
@router.put("/{user_id}", response_model=UserDetail, dependencies=[Depends(get_db)])
def update_user(user_id: int, user_update: UserUpdate):
    """
    根据用户 ID 更新用户信息
    """
    user = User.get_or_none(User.id == user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")

    # 更新用户信息
    user_data = user_update.dict(exclude_unset=True)  # 仅更新提供的字段
    for key, value in user_data.items():
        setattr(user, key, value)

    # 保存到数据库
    user.save()

    return user