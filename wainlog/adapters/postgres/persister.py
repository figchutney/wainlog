import datetime
from typing import List

from sqlalchemy.orm import Session

from ...core import types
from . import model
from .convertors import fell_db_to_app

#######
# GET #
#######


def get_user_db_from_username(session: Session, username: str) -> model.User:

    return (
        session.query(model.User)
        .filter(model.User.username == username)
        .one_or_none()
    )


def get_user_db_from_email(session: Session, email: str) -> model.User:

    return (
        session.query(model.User)
        .filter(model.User.email == email)
        .one_or_none()
    )


def get_user_db_from_id(session: Session, id: int) -> model.User:

    return session.query(model.User).filter(model.User.id == id).one_or_none()


def get_all_fells(session: Session) -> List[types.Fell]:

    fells = session.query(model.Fell).all()

    return [fell_db_to_app(fell=fell) for fell in fells]


def get_fell_id_from_name(session: Session, fell_name: types.FellName) -> int:

    return (
        session.query(model.Fell.id).filter(fell_name == model.Fell.name).one()
    )[0]


def get_summit_events_for_user(
    session: Session, username: str
) -> List[types.SummitEvent]:

    summit_events = (
        session.query(
            model.User.username,
            model.Fell.name,
            model.SummitEvent.summit_date,
        )
        .join(model.Fell.summit_events)
        .filter(username == model.User.username)
    ).all()

    return [
        types.SummitEvent(
            username=event.username,
            fell_name=event.name,
            summit_date=event.summit_date,
        )
        for event in summit_events
    ]


#######
# ADD #
#######


def add_user(session: Session, user: model.User) -> None:
    session.add(user)


def add_summit_event(
    session: Session,
    user_id: int,
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
    user_id: int,
    fell_name: types.FellName,
) -> None:

    fell_id = get_fell_id_from_name(session=session, fell_name=fell_name)
    summit_event = session.get(model.SummitEvent, (user_id, fell_id))

    session.delete(summit_event)
