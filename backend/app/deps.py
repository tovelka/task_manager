from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .database import get_db
from .models import User
from .services.jwt import decode_token
from .services.cookies import get_access_token


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

    result = user

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                'code': 'USER_NOT_FOUND',
                'message': 'Пользователь не найден',
            },
        )

    return user
