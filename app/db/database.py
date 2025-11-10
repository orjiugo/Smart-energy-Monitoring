"""Database connection and session management"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
from app.config import settings

engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    poolclass=NullPool if settings.environment == "testing" else None,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def get_db() -> Session:
    """Dependency to get database session for API routes"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()