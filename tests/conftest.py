import pytest

from app.database import get_db
from app.models import Movie
from app.schemas import MovieSchema


@pytest.fixture
def movie_a():
    return Movie(
        show_id="s2",
        title="7:19",
        director="Jorge Michel Grau",
        cast="Demián Bichir, Héctor Bonilla, Oscar Serrano, Azalia Ortiz, Octavio Michel, Carmen Beato",
        country="Mexico",
        date_added="December 23, 2016",
        release_year="2016",
        rating="TV-MA",
        duration="93 min",
        listed_in="Dramas, International Movies",
        description="After a devastating earthquake hits Mexico City, trapped survivors from all walks of life wait to be rescued while trying desperately to stay alive.",
    )

@pytest.fixture
def movie_b():
    return Movie(
        show_id="s3",
        title="23:59",
        director="Gilbert Chan",
        cast="Tedd Chan, Stella Chung, Henley Hii, Lawrence Koh, Tommy Kuan, Josh Lai, Mark Lee, Susan Leong, Benjamin Lim",
        country="Singapore",
        date_added="December 20, 2018",
        release_year="2011",
        rating="R",
        duration="78 min",
        listed_in="Horror Movies, International Movies",
        description="When an army recruit is found dead, his fellow soldiers are forced to confront a terrifying secret that's haunting their jungle island training camp.",
    )

@pytest.fixture
def movie_schema_a(movie_a):
    return MovieSchema.from_orm(movie_a)

@pytest.fixture
def movie_schema_b(movie_b):
    return MovieSchema.from_orm(movie_b)

db = pytest.fixture(get_db)

@pytest.fixture
def db_movies(db, movie_a, movie_b):
    db.query(Movie).delete() # make sure the db only has the expected values
    movies = (
        movie_a,
        movie_b,
    )
    db.add_all(movies)
    db.commit()
    return movies
