from fastapi import APIRouter, Depends

from ..models import User
from ..schemas.auth import UserResponse
from ..deps import get_current_user

router = APIRouter(prefix='/auth', tags=['users'])


@router.get('/me')
async def get_me(user: User = Depends(get_current_user)) -> UserResponse:
    """Получить текущего пользователя"""
    return user
