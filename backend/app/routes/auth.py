from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User
from ..schemas.auth import UserCreate, UserResponse, Tokens, UserLogin
from ..deps import get_current_user, get_db, get_user_service
from ..services import cookies, jwt
from ..services.auth import UserService
from ..exceptions import (
    NotFoundException,
    AccessDeniedException,
    DuplicateException,
)

router = APIRouter(prefix='/auth', tags=['users'])


@router.get('/me')
async def get_me(user: User = Depends(get_current_user)) -> UserResponse:
    """Получить текущего пользователя"""
    return user


@router.post(
    '/register/',
    status_code=201,
)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    user_service = UserService(db)
    try:
        user = await user_service.create(user_data)
    except DuplicateException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.details)
    await db.commit()
    return UserResponse.model_validate(user)


@router.post('/login/')
async def login(
    user_data: UserLogin,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    user_service = UserService(db)
    try:
        user = await user_service.authenticate_user(
            user_data.username, user_data.password
        )
    except (NotFoundException, AccessDeniedException):
        raise HTTPException(
            status_code=401,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = jwt.create_access_token(user.id)
    refresh_token = jwt.create_refresh_token(user.id)
    cookies.set_auth_cookies(response, access_token, refresh_token)
    return {'message': 'Вход выполнен'}


@router.post('/logout/', status_code=204)
async def logout(
    response: Response,
):
    cookies.clear_auth_cookies(response)
    return JSONResponse(content=None)


@router.post('/refresh_token/')
async def refresh_access_token(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    """Обновление access токена."""
    user_service = UserService(db)

    refresh_token = cookies.get_refresh_token_from_cookies(request)
    if not refresh_token:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail='Требуется повторный вход'
        )

    payload = jwt.decode_token(refresh_token)
    if payload is None or payload.get('type') != 'refresh':
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, 'Невалидный refresh токен'
        )

    token_hash = jwt.hash_refresh_token(refresh_token)

    try:
        stored = await user_service.get_users_refresh_token(token_hash)
    except NotFoundException as exc:
        cookies.clear_auth_cookies(response)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=exc.details)

    stored.revoked = True

    user = await user_service.get_user_by_id(stored.user_id)
    if user is None:
        cookies.clear_auth_cookies(response)
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, 'Пользователь не найден'
        )

    tokens: Tokens = await user_service.create_tokens(user)
    cookies.set_auth_cookies(
        response, tokens.access_token, tokens.refresh_token
    )
    await db.commit()
    return {'message': 'Токены обновлены'}
