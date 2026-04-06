from sqlmodel import create_engine, SQLModel, Session

from app.core.config import settings


engine = create_engine(settings.database_url, echo=True)


def create_db_and_tables():
    """Create database tables if they don't exist."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get a database session."""
    with Session(engine) as session:
        yield session