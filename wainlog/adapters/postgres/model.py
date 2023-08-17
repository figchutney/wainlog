from datetime import date, datetime

from flask_login import UserMixin
from sqlalchemy import ForeignKey, types
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)
from werkzeug.security import check_password_hash, generate_password_hash

from ...core.types import Book, FellName


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class User(UserMixin, Base, kw_only=True):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        types.Integer(), primary_key=True, init=False
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
    password_hash: Mapped[str] = mapped_column(
        types.String(128),
        nullable=False,
        init=False,
    )
    created_timestamp: Mapped[datetime] = mapped_column(
        types.DateTime(timezone=True),
        index=True,
        nullable=False,
        default=datetime.utcnow,
    )

    summit_events: Mapped[list["SummitEvent"]] = relationship(
        "SummitEvent",
        back_populates="user",
        uselist=True,
        default_factory=list,
    )  # TODO: Set `lazy="raise"`

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Fell(Base, kw_only=True):
    __tablename__ = "fell"

    id: Mapped[int] = mapped_column(
        types.Integer(),
        primary_key=True,
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
        back_populates="fell",
        uselist=True,
        default_factory=list,
    )  # TODO: Set `lazy="raise"`


class SummitEvent(Base, kw_only=True):
    __tablename__ = "summit_event"

    user_id: Mapped[int] = mapped_column(
        types.Integer(),
        ForeignKey("user.id"),
        primary_key=True,
    )
    fell_id: Mapped[int] = mapped_column(
        types.Integer(),
        ForeignKey("fell.id"),
        primary_key=True,
    )
    summit_date: Mapped[date] = mapped_column(
        types.Date(),
        nullable=False,
    )
    created_timestamp: Mapped[datetime] = mapped_column(
        types.DateTime(timezone=True),
        nullable=False,
        index=True,
        default=datetime.utcnow,
    )
