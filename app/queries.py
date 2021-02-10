from enum import Enum
from typing import List

from sqlalchemy import or_
from sqlalchemy.orm import Session

from .models import Movie
from .schemas import MovieSchema


FILTER_FIELD_NAMES = {
    "title",
    "director",
    "country",
    "release_year",
    # all other fields prohibited
}
SEARCH_FIELD_NAMES = {
    *FILTER_FIELD_NAMES,
    "cast",
    "description",
}
SORT_FIELD_NAMES = {
    "show_id",
    "release_year",
}
SORT_FIELD_KEYS = SORT_FIELD_NAMES | {
    f"-{name}"
    for name in SORT_FIELD_NAMES
}
ALLOWED_SORT_KEYS = Enum('SortKeys', {
    key: key
    for key in SORT_FIELD_KEYS
})


def get_movie(db: Session, show_id: str) -> Movie:
    return db.query(Movie).filter(Movie.show_id == show_id).first()


def filter_movies(
        db: Session,
        filters: dict,
        search: str = None,
        sort: str = None,
        skip: int = 0,
        limit: int = 100
):
    query = db.query(Movie)

    for name, value in filters.items(): # filter keys validated in endpoint
        query = query.filter(_get_field(name) == value)

    if search:
        query = query.filter(or_(*[
            search == _get_field(field_name)
            for field_name in SEARCH_FIELD_NAMES
        ]))

    if sort:
        desc = sort.startswith('-')
        name = sort[1:] if desc else sort
        field = _get_field(name)
        query = query.order_by(field.desc() if desc else field)

    return query.offset(skip).limit(limit).all()


def update_movie(db: Session, movie: MovieSchema) -> None:
    update_dict = {
        _get_field(field_name): field_value
        for field_name, field_value in movie.dict().items()
    }
    db.query(Movie).filter(Movie.show_id == movie.show_id).update(
        update_dict,
        synchronize_session=False # just UPDATE, don't follow with SELECT
    )
    db.commit()


def create_movie(db: Session, movie: MovieSchema) -> Movie:
    record = Movie(**movie.dict())
    db.add(record)
    db.commit()
    # `db.refresh` usually here but not needed because there are no auto-generated fields
    return record


def summarize_movies(movies: List[Movie]) -> dict:
    # extreme bare minimum aggregate
    return {
        "movies": movies,
        "count": len(movies),
    }


def _get_field(field_name):
    return getattr(Movie, field_name)
