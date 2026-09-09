from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Event
from ..schemas.events import EventCreate, EventsList


class EventRepository:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_event_by_id(self, event_id: int) -> Event | None:
        result = await self.db.execute(
            select(Event).where(Event.id == event_id)
        )
        return result.scalar_one_or_none()

    async def get_events_by_user(self, user_id: int) -> list[Event]:
        result = await self.db.execute(
            select(Event).where(Event.created_by_id == user_id)
        )
        return list(result.scalars().all())

    async def create(
        self, event_data: EventCreate, password_hash: str
    ) -> Event:
        event_dict = event_data.model_dump(exclude={'password'})
        event_dict['password_hash'] = password_hash
        db_event = Event(**event_dict)
        await self.db.flush()
        await self.db.refresh(db_event)
        return db_event
