from fastapi import HTTPException
from sqlalchemy.orm import Session

from .models import Movie
from .schemas import MovieSchema


MODEL_FILTERS = {
    "title": Movie.title
    "director": Movie.director,
    "country": Movie.country,
    "release_year": Movie.release_year,
    # all other fields prohibited
}


def get_movie(db: Session, show_id: str):
    return db.query(Movie).filter(Movie.show_id == show_id).first()


def filter_movies(db: Session, request_filters: dict, skip: int = 0, limit: int = 100):
    disallowed_keys = request_filters.keys() - FILTERS.keys()
    if disallowed_keys:
        raise HTTPException(
            status_code=400,
            detail="Filtering not supported on {}".format(disallowed_keys)
        )
    filters = {
        model_field: request_filters[filter_name]
        for filter_name, model_field in MODEL_FILTERS.items()
        if filter_name in request_filters.items()
    }
    return db.query(Movie).filter(**filters).offset(skip).limit(limit).all()


def update_movie(db: Session, movie: MovieSchema):
    update_dict = {
        getattr(Movie, field_name): field_value
        for field_name, field_value in movie.dict()
    }
    db.query(Movie).filter(Movie.show_id == movie.show_id).update(
        update_dict,
        synchronize_session=False
    )


def create_movie(db: Session, movie: MovieSchema):
    row = Movie(**movie.dict())
    db.add(row)
    db.commit()
    return row


def summarize_movies(db: Session):
    pass
