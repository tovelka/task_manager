from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Event
from ..schemas.events import EventUpdate


class EventRepository:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_event_by_id(self, event_id: int) -> Event | None:
        result = await self.db.execute(
            select(Event).where(Event.id == event_id)
        )
        return result.scalar_one_or_none()

    async def get_events_by_user_id(self, user_id: int) -> list[Event]:
        result = await self.db.execute(
            select(Event).where(Event.created_by_id == user_id)
        )
        return list(result.scalars().all())

    async def create(self, event_dict: dict) -> Event:
        db_event = Event(**event_dict)
        self.db.add(db_event)
        await self.db.flush()
        await self.db.refresh(db_event)
        return db_event

    async def update(self, event: Event, event_data: EventUpdate) -> Event:
        event_dict = event_data.model_dump(exclude_unset=True)
        for key, value in event_dict.items():
            setattr(event, key, value)
        await self.db.flush()
        await self.db.refresh(event)
        return event

    async def delete(self, event: Event) -> bool:
        await self.db.delete(event)
        await self.db.flush()
        return True
