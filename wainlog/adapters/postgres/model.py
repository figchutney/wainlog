from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Column, ForeignKey, types
from sqlalchemy.orm import declarative_base, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from ...core.types import Book, FellName

Base = declarative_base()


class User(UserMixin, Base):

    __tablename__ = "user"

    id = Column(types.Integer(), primary_key=True)
    username = Column(
        types.String(64), index=True, unique=True, nullable=False
    )
    email = Column(types.String(120), index=True, unique=True, nullable=False)
    password_hash = Column(types.String(128), nullable=False)
    created_timestamp = Column(
        types.DateTime(timezone=True),
        index=True,
        nullable=False,
        default=datetime.utcnow,
    )

    summit_events = relationship("SummitEvent", backref="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Fell(Base):

    __tablename__ = "fell"

    id = Column(types.Integer(), primary_key=True)
    name = Column(types.Enum(FellName), index=True, unique=True)
    display = Column(types.String(50), unique=True)
    height_rank = Column(
        types.Integer(), unique=True
    )  # Used as some fells have the same height_m value
    height_m = Column(types.Integer(), unique=False)
    os_grid_reference = Column(types.String(8), unique=True)
    book = Column(types.Enum(Book), unique=False)
    rank_in_book = Column(types.Integer(), unique=False)

    summit_events = relationship("SummitEvent", backref="fell")


class SummitEvent(Base):

    __tablename__ = "summit_event"

    user_id = Column(types.Integer(), ForeignKey("user.id"), primary_key=True)
    fell_id = Column(types.Integer(), ForeignKey("fell.id"), primary_key=True)
    summit_date = Column(
        types.Date(),
        nullable=False,
    )
    created_timestamp = Column(
        types.DateTime(timezone=True),
        nullable=False,
        index=True,
        default=datetime.utcnow,
    )
