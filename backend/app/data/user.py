from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User, Event
from ..schemas.auth import UserCreate


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_user_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def get_user_with_events_by_userid(self, user_id: int) -> list[Event]:
        result = await self.db.execute(
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.events))
        )
        return list(result.scalars().all())

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user
