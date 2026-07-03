"""SQLAlchemy engine, session factory, and the declarative Base."""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from core.config import settings


# SQLite needs `check_same_thread=False` because FastAPI may run handlers
# across threads. MySQL/Postgres ignore this arg.
_connect_args: dict = {}
if settings.DATABASE_URL.startswith("sqlite"):
    _connect_args["check_same_thread"] = False

engine = create_engine(settings.DATABASE_URL, connect_args=_connect_args, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


def get_db():
    """FastAPI dependency: open a DB session for the request, close at the end."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
