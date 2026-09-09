from datetime import datetime, timedelta

import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from ..models import User, RefreshToken
from ..data.user import UserRepository
from ..data.refresh_tokens import RefreshTokensRepository
from ..schemas.auth import UserCreate, Tokens
from ..config import get_settings
from . import jwt
from ..exceptions import (
    NotFoundException,
    AccessDeniedException,
    DuplicateException,
)

settings = get_settings()


class UserService:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db
        self.user_repository = UserRepository(db)
        self.refresh_tokens_repository = RefreshTokensRepository(db)

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.user_repository.get_user_by_id(user_id)

    async def get_user_by_username(self, username: str) -> User | None:
        return await self.user_repository.get_user_by_username(username)

    async def create(self, user_data: UserCreate) -> User:
        hashed_password = self.hash_password(user_data.password)
        user_dict = user_data.model_dump(exclude={'password'})
        user_dict['password_hash'] = hashed_password
        db_user = User(**user_dict)
        try:
            new_user = await self.user_repository.create(db_user)
        except IntegrityError:
            raise DuplicateException(details='Имя пользователя занято.')
        return new_user

    async def authenticate_user(self, username: str, password: str) -> User:
        user = await self.user_repository.get_user_by_username(username)
        if not user:
            raise NotFoundException(details='Пользователь не найден')
        decoded_password = self.verify_password(password, user.password_hash)
        if not decoded_password:
            raise AccessDeniedException('Неверный пароль пользователя.')
        return user

    async def get_users_refresh_token(self, token_hash: str) -> RefreshToken:
        refresh_token = await self.refresh_tokens_repository.get_by_token_hash(
            token_hash
        )
        if not refresh_token:
            raise NotFoundException('Токен не найден или он устарел.')
        return refresh_token

    async def create_tokens(self, user: User) -> Tokens:
        """Создаёт токены, сохраняет в БД."""
        access = jwt.create_access_token(user.id)
        refresh = jwt.create_refresh_token(user.id)
        token = RefreshToken(
            user_id=user.id,
            token_hash=jwt.hash_refresh_token(refresh),
            expires_at=datetime.utcnow()
            + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )
        await self.refresh_tokens_repository.create(token)
        return Tokens(access_token=access, refresh_token=refresh)

    @staticmethod
    def hash_password(plain: str) -> str:
        """Хэширует пароль с использованием bcrypt."""
        password_bytes = plain.encode('utf-8')
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        """Проверяет пароль против хэша."""
        password_bytes = plain.encode('utf-8')
        hashed_bytes = hashed.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
