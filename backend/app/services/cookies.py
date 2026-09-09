"""Управление auth cookies (HttpOnly) и CSRF токенами."""

import secrets
from typing import Optional

from fastapi import Request, Response

from ..config import get_settings

settings = get_settings()

ACCESS_TOKEN_COOKIE = 'access_token'
REFRESH_TOKEN_COOKIE = 'refresh_token'


def set_auth_cookies(
    response: Response,
    access_token: str,
    refresh_token: str,
) -> bool:
    """
    Устанавливает все три куки:
    - access_token (HttpOnly) — для авторизации
    - refresh_token (HttpOnly) — для обновления access
    """

    common = dict(
        domain=settings.COOKIE_DOMAIN,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        path='/',
    )

    response.set_cookie(
        key=ACCESS_TOKEN_COOKIE,
        value=access_token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        **common,
    )

    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE,
        value=refresh_token,
        httponly=True,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
        **common,
    )

    return True


def clear_auth_cookies(response: Response) -> None:
    """Удаляет все три куки (при выходе)."""
    for cookie_name in [
        ACCESS_TOKEN_COOKIE,
        REFRESH_TOKEN_COOKIE,
    ]:
        response.delete_cookie(
            key=cookie_name,
            domain=settings.COOKIE_DOMAIN,
            path='/',
        )


def get_access_token(request: Request) -> Optional[str]:
    """Достаёт access_token из cookie запроса."""
    return request.cookies.get(ACCESS_TOKEN_COOKIE)


def get_refresh_token(request: Request) -> Optional[str]:
    """Достаёт refresh_token из cookie запроса."""
    return request.cookies.get(REFRESH_TOKEN_COOKIE)
