from datetime import datetime, timedelta
import jwt
import hashlib

from ..config import get_settings

settings = get_settings()


def create_access_token(user_id: int) -> str:
    payload = {
        'sub': str(user_id),
        'type': 'access',
        'exp': datetime.utcnow()
        + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        'iat': datetime.utcnow(),
    }
    return jwt.encode(
        payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )


def create_refresh_token(user_id: int) -> str:
    payload = {
        'sub': str(user_id),
        'type': 'refresh',
        'exp': datetime.utcnow()
        + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        'iat': datetime.utcnow(),
    }
    return jwt.encode(
        payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def hash_refresh_token(token: str) -> str:
    """Хэшируем refresh token перед сохранением в БД."""
    return hashlib.sha256(token.encode()).hexdigest()
