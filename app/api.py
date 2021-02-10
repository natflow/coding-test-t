from typing import Optional

from fastapi import Depends, APIRouter, HTTPException, Request
from sqlalchemy.orm import Session

from .database import get_db
from .models import Movie
from .queries import (
    ALLOWED_SORT_KEYS,
    create_movie,
    FILTER_FIELD_NAMES,
    filter_movies,
    get_movie,
    summarize_movies,
    update_movie,
)
from .schemas import MovieSchema, MoviesWithSummarySchema


router = APIRouter()

@router.get("/movies", response_model=MoviesWithSummarySchema)
def read_movies(
        request: Request,
        db: Session = Depends(get_db),
        search: Optional[str] = None,
        sort: Optional[ALLOWED_SORT_KEYS] = None,
        skip: Optional[int] = 0,
        limit: Optional[int] = 100
):
    filters = {
        k: v
        for k, v in request.query_params.items()
        if k in FILTER_FIELD_NAMES
    }
    movies = filter_movies(
        db,
        filters,
        search=search,
        sort=sort and sort.value,
        skip=skip,
        limit=limit
    )
    return summarize_movies(movies)

@router.get("/movies/{show_id}", response_model=MovieSchema)
def read_movie(show_id: str, db: Session = Depends(get_db)):
    db_movie = get_movie(db, show_id=show_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

@router.put("/movies/{show_id}", response_model=MovieSchema)
def put_movie(movie: MovieSchema, db: Session = Depends(get_db)):
    db_movie = get_movie(db, show_id=movie.show_id)
    if db_movie is None:
        create_movie(db, movie)
    else:
        update_movie(db, movie)
    return movie
