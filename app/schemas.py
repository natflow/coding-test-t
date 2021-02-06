from datetime import date

from pydantic import BaseModel


class MovieSchema(BaseModel):
    # TODO: maybe add strictness to types
    show_id: str
    # type: str = Literal("Movie")
    title: str
    director: str
    cast: str
    country: str
    date_added: date # TODO: parsing/formatting; pendulum.parse("April 1, 2019", strict=False)
    release_year: str
    rating: str
    duration: str
    listed_in: str
    description: str

    class Config:
        orm_mode = True
