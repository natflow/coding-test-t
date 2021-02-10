from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from .database import engine


Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"

    show_id = Column(String, primary_key=True, index=True)
    title = Column(String)
    director = Column(String)
    cast = Column(String)
    country = Column(String)
    date_added = Column(String) # not DateTime because it's stored like "April 1, 2019"
    release_year = Column(Integer)
    rating = Column(String)
    duration = Column(String)
    listed_in = Column(String)
    description = Column(String)


Base.metadata.create_all(bind=engine)
