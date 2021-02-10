from typing import List

from fastapi import HTTPException
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
ALLOWED_FILTER_NAMES = Enum('FilterKeys', {
    name: name
    for name in FILTER_FIELD_NAMES
})
SEARCH_FIELD_NAMES = {
    *FILTER_FIELD_NAMES,
    "cast",
    "description",
}
SORT_FIELD_NAMES = {
    "show_id",
    "release_year",
}
SORT_FIELD_KEYS = SORT_FIELD_NAMES + {
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
        skip: int = 0,
        limit: int = 100,
        sort: str = None
):
    query = db.query(Movie)

    if filters:
        disallowed_keys = filters.keys() - FILTER_FIELD_NAMES
        if disallowed_keys:
            raise HTTPException(
                status_code=400,
                detail=f"Filtering not supported on {disallowed_keys}"
            )
        model_filters = {
            _get_field(name): filters[name]
            for name in FILTER_FIELD_NAMES
            if name in filters.keys()
        }
        query = query.filter(**model_filters)

    if search:
        for field in map(_get_field, SEARCH_FIELD_NAMES):
            query |= query.filter(search in field)

    if sort:
        desc = sort.startswith('-')
        name = sort[1:] if desc else sort
        field = _get_field(name)
        query = query.order_by(field.desc() if desc else field)

    return query.offset(skip).limit(limit).all()


def update_movie(db: Session, movie: MovieSchema) -> None:
    update_dict = {
        _get_field(field_name): field_value
        for field_name, field_value in movie.dict()
    }
    db.query(Movie).filter(Movie.show_id == movie.show_id).update(
        update_dict,
        synchronize_session=False
    )


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
