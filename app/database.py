import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

engine = create_engine(
    os.environ.get("SQLALCHEMY_DATABASE_URL", "sqlite:///./movies.db"),
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
    # use the same connection across all threads, so tests can use the same in-memory database
    # https://docs.sqlalchemy.org/en/13/dialects/sqlite.html#using-a-memory-database-in-multiple-threads
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
