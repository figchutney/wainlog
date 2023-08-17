from sqlalchemy.orm import Session

from ...core import types
from ..postgres import persister


def get_fells_by_book(session: Session) -> dict[types.Book, list[types.Fell]]:
    fells_by_book: dict[types.Book, list[types.Fell]] = {
        types.Book.EASTERN: [],
        types.Book.FAR_EASTERN: [],
        types.Book.CENTRAL: [],
        types.Book.SOUTHERN: [],
        types.Book.NORTHERN: [],
        types.Book.NORTH_WESTERN: [],
        types.Book.WESTERN: [],
    }

    for fell in persister.get_all_fells(session=session):
        fells_by_book[fell.book].append(fell)

    for fells in fells_by_book.values():
        fells.sort(key=lambda x: x.rank_in_book)

    return fells_by_book
