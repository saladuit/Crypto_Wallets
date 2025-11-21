""""Pytest fixtures for testing with FastAPI and SQLAlchemy."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app import app  # import the FastAPI app
from backend.db.wallet import Base, DBWallet  # import your Base to create tables
from backend.db.get_db import get_db  # import the get_db dependency

# Use an in-memory SQLite DB that is usable across threads
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    """Create the database schema once for the test session and tear down after.

    This creates tables on the in-memory `engine` used by the tests. The
    TestClient override below will yield the transactional `db_session`, so
    it's important the schema exists on the same engine/connection.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

@pytest.fixture
def wallet_factory(db_session):
    """Factory to create wallets in the test database."""
    def _create(address: str = "0xabc", expected_quantity: float = 0.0, currency: str = "ETH"):
        w = DBWallet(address=address, expected_quantity=expected_quantity, currency=currency)
        db_session.add(w)
        db_session.commit()
        db_session.refresh(w)
        return w
    return _create

@pytest.fixture()
def db_session():
    """
    Yield a SQLAlchemy session for direct DB tests (if needed).
    """
    connection = engine.connect()
    connection.begin()
    session = SessionTesting(bind=connection)
    try:
        yield session
    finally:
        session.close()
        connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    """
    Create a new FastApi TestClient htat uses the `db_session` fixture
    to override the `get_db` dependency that is injected into routes.
    """

    # dependency override generator
    # Make the app use the same transactional session as the test.
    def override_get_db():
        try:
            yield db_session
        finally:
            # db_session is closed/rolled back by the db_session fixture
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

    # cleanup override to avoid leaking between tests
    app.dependency_overrides.pop(get_db, None)
