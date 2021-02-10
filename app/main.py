from typing import Dict, Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from .models import Movie
from .schemas import MovieSchema, MoviesWithSummarySchema
from .queries import (
    ALLOWED_SORT_KEYS,
    ALLOWED_FILTER_NAMES,
    create_movie,
    filter_movies,
    get_movie,
    summarize_movies,
    update_movie,
)


app = FastAPI()


@app.get("/movies", response_model=MoviesWithSummarySchema)
def read_movies(
        db: Session = Depends(get_db),
        skip: Optional[int] = 0,
        limit: Optional[int] = 100,
        sort: Optional[ALLOWED_SORT_KEYS] = None,
        search: Optional[str] = None,
        **filters: Optional[Dict[ALLOWED_FILTER_NAMES, str]]
):
    movies = filter_movies(db, skip=skip, limit=limit)
    return summarize_movies(movies)


@app.get("/movies/{show_id}", response_model=MovieSchema)
def read_movie(show_id: int, db: Session = Depends(get_db)):
    db_movie = get_movie(db, show_id=show_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie


@app.put("/movies/{show_id}", response_model=MovieSchema)
def put_movie(movie: MovieSchema, db: Session = Depends(get_db)):
    db_movie = get_movie(db, movie.show_id)
    if db_movie is not None:
        update_movie(db, movie)
    else:
        create_movie(db, movie)
    return movie
