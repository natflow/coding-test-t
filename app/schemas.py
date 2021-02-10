from typing import List

from pydantic import BaseModel


class MovieSchema(BaseModel):
    show_id: str
    # type: Literal["Movie"]
    title: str
    director: str
    cast: str
    country: str
    date_added: str # stored like "April 1, 2019", so not directly parseable to date type
    release_year: str
    rating: str
    duration: str
    listed_in: str
    description: str

    class Config:
        orm_mode = True


class MoviesWithSummarySchema(BaseModel):
    movies: List[MovieSchema]
    count: int
