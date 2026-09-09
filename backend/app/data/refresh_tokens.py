from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import RefreshToken, User


class RefreshTokensRepository:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_by_token_hash(self, token_hash: str) -> RefreshToken | None:
        result = await self.db.execute(
            select(RefreshToken)
            .where(
                RefreshToken.token_hash == token_hash,
                RefreshToken.revoked == False,
                RefreshToken.expires_at > datetime.utcnow(),
            )
            .options(selectinload(RefreshToken.user))
        )
        return result.scalar_one_or_none()

    async def create(self, refresh_token: RefreshToken) -> RefreshToken:
        self.db.add(refresh_token)
        await self.db.flush()
        await self.db.refresh(refresh_token)
        return refresh_token
