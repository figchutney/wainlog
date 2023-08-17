import uuid
from datetime import date, datetime

from flask_login import UserMixin
from sqlalchemy import ForeignKey, func, types
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)

from ...core.types import Book, FellName


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class User(UserMixin, Base, kw_only=True):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
        default=uuid.uuid4,
        init=False,
    )
    username: Mapped[str] = mapped_column(
        types.String(64),
        index=True,
        unique=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        types.String(120),
        index=True,
        unique=True,
        nullable=False,
    )
    created_timestamp: Mapped[datetime] = mapped_column(
        types.DateTime,
        index=True,
        nullable=False,
        default=None,
        server_default=func.now(),
    )

    summit_events: Mapped[list["SummitEvent"]] = relationship(
        "SummitEvent",
        backref="user",
        uselist=True,
        default_factory=list,
    )  # TODO: Set `lazy="raise"`


class Fell(Base, kw_only=True):
    __tablename__ = "fell"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
        default=uuid.uuid4,
    )
    name: Mapped[FellName] = mapped_column(
        types.Enum(FellName),
        index=True,
        unique=True,
    )
    display: Mapped[str] = mapped_column(types.String(50), unique=True)
    height_rank: Mapped[int] = mapped_column(
        types.Integer(),
        unique=True,
    )  # Used as some fells have the same height_m value
    height_m: Mapped[int] = mapped_column(
        types.Integer(),
        unique=False,
    )
    os_grid_reference: Mapped[str] = mapped_column(
        types.String(8),
        unique=True,
    )
    book: Mapped[Book] = mapped_column(
        types.Enum(Book),
        unique=False,
    )
    rank_in_book: Mapped[int] = mapped_column(
        types.Integer(),
        unique=False,
    )

    summit_events: Mapped[list["SummitEvent"]] = relationship(
        "SummitEvent",
        backref="fell",
        uselist=True,
        default_factory=list,
    )  # TODO: Set `lazy="raise"`


class SummitEvent(Base, kw_only=True):
    __tablename__ = "summit_event"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id"),
        primary_key=True,
    )
    fell_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("fell.id"),
        primary_key=True,
    )
    summit_date: Mapped[date] = mapped_column(
        types.Date(),
        nullable=False,
    )
    created_timestamp: Mapped[datetime] = mapped_column(
        types.DateTime,
        index=True,
        nullable=False,
        default=None,
        server_default=func.now(),
    )
