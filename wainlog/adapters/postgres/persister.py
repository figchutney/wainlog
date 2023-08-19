import datetime
import uuid
from typing import cast

from sqlalchemy.orm import Session

from ...core import types
from . import model
from .convertors import fell_db_to_app

#######
# GET #
#######


def get_user_db_from_email(
    session: Session,
    email: str,
) -> model.User | None:
    return (
        session.query(model.User)
        .filter(model.User.email == email)
        .one_or_none()
    )


def get_user_db_from_id(
    session: Session,
    id: uuid.UUID,
) -> model.User | None:
    return session.query(model.User).filter(model.User.id == id).one_or_none()


def get_all_fells(session: Session) -> list[types.Fell]:
    fells = session.query(model.Fell).all()

    return [fell_db_to_app(fell=fell) for fell in fells]


def get_fell_id_from_name(
    session: Session,
    fell_name: types.FellName,
) -> uuid.UUID:
    return cast(
        uuid.UUID,
        (
            session.query(model.Fell.id)
            .filter(model.Fell.name == fell_name)
            .one()
        )[0],
    )


def get_summit_events_for_user(
    session: Session,
    username: str,
) -> list[types.SummitEvent]:
    rows = (
        session.query(
            model.SummitEvent, model.User.username, model.Fell.name
        )
        .join(model.User, model.User.id == model.SummitEvent.user_id)
        .join(model.Fell, model.Fell.id == model.SummitEvent.fell_id)
        .filter(model.User.username == username)
    ).all()

    return [
        types.SummitEvent(
            username=username,
            fell_name=fell_name,
            summit_date=event.summit_date,
        )
        for event, username, fell_name in rows
    ]


#######
# ADD #
#######


def add_user(
    session: Session,
    user: model.User,
) -> None:
    session.add(user)


def add_summit_event(
    session: Session,
    user_id: uuid.UUID,
    fell_name: types.FellName,
    summit_date: datetime.date,
) -> None:
    fell_id = get_fell_id_from_name(session=session, fell_name=fell_name)

    session.add(
        model.SummitEvent(
            user_id=user_id,
            fell_id=fell_id,
            summit_date=summit_date,
        )
    )


##########
# DELETE #
##########


def delete_summit_event(
    session: Session,
    user_id: uuid.UUID,
    fell_name: types.FellName,
) -> None:
    fell_id = get_fell_id_from_name(session=session, fell_name=fell_name)
    summit_event = session.get(model.SummitEvent, (user_id, fell_id))

    session.delete(summit_event)
