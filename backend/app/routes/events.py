# backend/app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User, Event, EventStatus
from ..schemas.events import (
    EventListResponse,
    EventResponse,
    EventCreate,
    EventDelete,
    EventUpdate,
)
from ..deps import get_current_user, get_db, get_user_service
from ..services.events import EventService
from ..services.auth import UserService
from ..exceptions import (
    NotFoundException,
    AccessDeniedException,
    UncorrectDataException,
)

router = APIRouter(prefix='/events', tags=['events'])


@router.get('/{event_id}')
async def get_by_id(
    event_id,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> EventResponse:
    """
    Получает событие по id (просмотр разрешен только автору).
    """
    event_service = EventService(db)
    try:
        event = await event_service.get_by_id(event_id, current_user.id)
    except (AccessDeniedException, NotFoundException):
        raise HTTPException(status_code=404, detail='Такое событие не найдено.')
    return EventResponse.model_validate(event)


@router.get('/')
async def get_all(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> EventListResponse:
    """
    Получает все события текущего пользователя.
    """
    event_service = EventService(db)
    try:
        events = await event_service.get_all(current_user.id)
    except AccessDeniedException:
        raise HTTPException(status_code=404, detail='Такое событие не найдено.')
    events_responses = [EventResponse.model_validate(event) for event in events]
    return EventListResponse(events=events_responses, count=len(events))


@router.patch('/{event_id}')
async def update(
    event_id: int,
    event_data: EventUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> EventResponse:
    """
    Обновляет событие (доступно только автору).
    """
    event_service = EventService(db)
    try:
        event = await event_service.update(
            event_id, event_data, current_user.id
        )
    except (AccessDeniedException, NotFoundException):
        raise HTTPException(status_code=404, detail='Такое событие не найдено.')
    await db.commit()
    return EventResponse.model_validate(event)


@router.post('/')
async def create(
    event_data: EventCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> EventResponse:
    """
    Создает событие (доступно только аутентифицируемому пользователю).
    """
    event_service = EventService(db)
    try:
        event = await event_service.create(event_data, current_user.id)
    except UncorrectDataException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.details)
    await db.commit()
    return EventResponse.model_validate(event)


@router.delete('/{event_id}')
async def delete(
    event_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> bool:
    """
    Удаляет событие (доступно только автору).
    """
    event_service = EventService(db)
    try:
        result = await event_service.delete(event_id, current_user)
    except (AccessDeniedException, NotFoundException):
        raise HTTPException(status_code=404, detail='Такое событие не найдено.')
    await db.commit()
    return result
