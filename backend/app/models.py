import enum
from datetime import datetime
from sqlalchemy import (
    String,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    Enum as SQLEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class User(Base):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    username: Mapped[str] = mapped_column(
        String(32), nullable=False, unique=True
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    refresh_tokens: Mapped[list['RefreshToken']] = relationship(
        back_populates='user',
        cascade='all',
        lazy='noload',
    )


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False
    )
    token_hash: Mapped[str] = mapped_column(
        String(64), unique=True, index=True, nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped['User'] = relationship(
        back_populates='refresh_tokens',
        lazy='noload',
    )


class EventStatus(str, enum.Enum):
    PLANNED = 'planned'
    ONGOING = 'ongoing'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'


class Event(Base):
    title: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    status: Mapped[EventStatus] = mapped_column(
        SQLEnum(EventStatus), default=EventStatus.PLANNED
    )

    created_by_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('User.id', ondelete='CASCADE'), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    ends_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    user: Mapped['User'] = relationship(
        back_populates='events',
        lazy='noload',
    )
