from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from ..data import user, events
from ..models import Event, EventStatus
from ..config import get_settings
from ..exceptions import (
    NotFoundException,
    AccessDeniedException,
    UncorrectDataException,
)
from ..schemas.events import EventUpdate, EventCreate

settings = get_settings()


class EventService:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db
        self.event_repository = events.EventRepository(db)
        self.user_repository = user.UserRepository(db)

    async def get_by_id(self, event_id: int, current_user_id: int) -> Event:
        event = await self.event_repository.get_event_by_id(event_id)
        if not event:
            raise NotFoundException(details='Событие в бд не найдено.')
        if event.created_by_id != current_user_id:
            raise AccessDeniedException(
                details='Событие принадлежит другому пользователю.'
            )
        return event

    async def get_all(self, current_user_id: int) -> list[Event]:
        return await self.event_repository.get_events_by_user_id(
            current_user_id
        )

    async def update(
        self, event_id: int, event_data: EventUpdate, current_user_id: int
    ) -> Event:
        event = await self.event_repository.get_event_by_id(event_id)
        if not event:
            raise NotFoundException(details='Событие в бд не найдено.')
        if event.created_by_id != current_user_id:
            raise AccessDeniedException(
                details='Событие принадлежит другому пользователю.'
            )
        return await self.event_repository.update(event, event_data)

    async def create(
        self, event_data: EventCreate, current_user_id: int
    ) -> Event:
        if event_data.starts_at > event_data.ends_at:
            raise UncorrectDataException(
                details='Начало события не может быть позже его окончания.'
            )
        event_dict = event_data.model_dump()
        event_dict['created_by_id'] = current_user_id
        current_datetime = datetime.utcnow()
        event_dict['status'] = (
            EventStatus.PLANNED
            if event_data.starts_at > current_datetime
            else EventStatus.ONGOING
            if event_data.ends_at > current_datetime
            else EventStatus.COMPLETED
        )
        return await self.event_repository.create(event_dict)

    async def delete(self, event_id: int, current_user_id: int) -> bool:
        event = await self.event_repository.get_event_by_id(event_id)
        if not event:
            raise NotFoundException(details='Событие в бд не найдено.')
        if event.created_by_id != current_user_id:
            raise AccessDeniedException(
                details='Событие принадлежит другому пользователю.'
            )
        return await self.event_repository.delete(event)
