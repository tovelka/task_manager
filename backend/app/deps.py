from fastapi import HTTPException, Request, status, Depends

from .database import get_db
from .models import User
from .services.jwt import decode_token
from .services.cookies import get_access_token
from .services.auth import UserService


user_service = UserService(Depends(get_db))


async def get_current_user(
    request: Request,
) -> User:
    """Достаёт текущего пользователя из HttpOnly cookie."""
    token = get_access_token(request)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                'code': 'NOT_AUTHENTICATED',
                'message': 'Требуется авторизация',
            },
        )

    payload = decode_token(token)
    if payload is None or payload.get('type') != 'access':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                'code': 'INVALID_TOKEN',
                'message': 'Невалидный или истёкший токен',
            },
        )

    try:
        user_id = int(payload['sub'])
    except (ValueError, KeyError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                'code': 'INVALID_TOKEN',
                'message': 'Невалидный токен',
            },
        )

    user = await user_service.get_user_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                'code': 'USER_NOT_FOUND',
                'message': 'Пользователь не найден',
            },
        )

    return user


def get_user_service():
    return UserService(Depends(get_db))
