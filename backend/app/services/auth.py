from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User
from ..data.user import UserRepository


class UserService:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db
        self.user_repository = UserRepository(db)

    async def get_user_by_id(self, user_id: int) -> User:
        return self.user_repository.get_user_by_id(user_id)

    async def get_user_by_username(self, username: str) -> User | None:
        return self.user_repository.get_user_by_username(username)
