from ...core import types
from . import model


def user_db_to_app(user: model.User) -> types.User:
    return types.User(
        username=user.username,
        email=user.email,
    )


def fell_db_to_app(fell: model.Fell) -> types.Fell:
    return types.Fell(
        name=fell.name,
        display=fell.display,
        height_rank=fell.height_rank,
        height_m=fell.height_m,
        height_f=int(fell.height_m * 3.28084),
        os_grid_reference=fell.os_grid_reference,
        book=fell.book,
        rank_in_book=fell.rank_in_book,
    )
