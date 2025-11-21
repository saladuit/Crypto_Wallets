"""Database session dependency."""

from backend.db.wallet import SessionLocal

def get_db():
    """Yield a database session and ensure it is closed after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()