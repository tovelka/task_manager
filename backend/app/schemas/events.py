from datetime import datetime

from pydantic import BaseModel


class EventBase(BaseModel):
    title: str
    description: str | None = None
    starts_at: datetime
    ends_at: datetime


class EventCreate(EventBase): ...


class EventUpdate(EventBase): ...


class EventResponse(EventBase):
    id: int


class EventListResponse(BaseModel):
    events: list[EventResponse]
    count: int
