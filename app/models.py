from sqlalchemy import Column, Integer, String, DateTime

from .database import Base


class Movie(Base):
    __tablename__ = "movies"

    show_id = Column(String, primary_key=True, index=True)
    #type = Column(String) # always "Movie"
    title = Column(String)
    director = Column(String)
    cast = Column(String)
    country = Column(String)
    date_added = Column(DateTime)
    release_year = Column(Integer)
    rating = Column(String)
    duration = Column(String)
    listed_in = Column(String)
    description = Column(String)
