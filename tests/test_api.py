from fastapi.testclient import TestClient
import pytest

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_insertion(client, movie_a, movie_schema_a):
    movie_data = movie_schema_a.dict()

    assert client.get(f"/movies/{movie_a.show_id}").status_code == 404

    resp = client.put(f"/movies/{movie_a.show_id}", json=movie_data)
    assert resp.status_code == 200
    assert resp.json() == movie_data

    resp = client.get(f"/movies/{movie_a.show_id}")
    assert resp.status_code == 200
    assert resp.json() == movie_data

    resp = client.get("/movies")
    assert resp.status_code == 200
    assert resp.json() == {
        "count": 1,
        "movies": [movie_data],
    }

def test_modification(client, movie_a, movie_schema_a):
    movie_data = movie_schema_a.dict()

    resp = client.put(f"/movies/{movie_a.show_id}", json=movie_data)
    assert resp.status_code == 200
    assert resp.json() == movie_data

    modified_data = {
        **movie_data,
        "title": "a new title",
    }
    resp = client.put(f"/movies/{movie_a.show_id}", json=modified_data)
    assert resp.status_code == 200
    assert resp.json() == modified_data

    resp = client.get(f"/movies/{movie_a.show_id}")
    assert resp.status_code == 200
    assert resp.json() == modified_data

def test_sorting(client, db_movies, movie_schema_a, movie_schema_b):
    movie_a = movie_schema_a.dict()
    movie_b = movie_schema_b.dict()

    resp = client.get("/movies", params={
        "sort": "-show_id",
    })
    assert resp.status_code == 200
    assert resp.json() == {
        "count": 2,
        "movies": [movie_b, movie_a],
    }

def test_search(client, db_movies, movie_schema_b):
    movie_b = movie_schema_b.dict()

    resp = client.get("/movies", params={
        "search": "23:59",
    })
    assert resp.status_code == 200
    assert resp.json() == {
        "count": 1,
        "movies": [movie_b],
    }

def test_filter(client, db_movies, movie_schema_b):
    movie_b = movie_schema_b.dict()

    resp = client.get("/movies", params={
        "director": "Gilbert Chan",
    })
    assert resp.status_code == 200
    assert resp.json() == {
        "count": 1,
        "movies": [movie_b],
    }

def test_pagination(client, db_movies, movie_schema_a, movie_schema_b):
    movie_a = movie_schema_a.dict()
    movie_b = movie_schema_b.dict()

    resp = client.get("/movies", params={
        "sort": "show_id",
        "limit": 1,
    })
    assert resp.status_code == 200
    assert resp.json() == {
        "count": 1,
        "movies": [movie_a],
    }

    resp = client.get("/movies", params={
        "sort": "show_id",
        "skip": 1,
    })
    assert resp.status_code == 200
    assert resp.json() == {
        "count": 1,
        "movies": [movie_b],
    }
