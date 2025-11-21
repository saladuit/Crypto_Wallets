"""Database models for Wallet."""

from sqlalchemy import Integer, String, Float, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


DATABASE_URL = "sqlite:///wallets.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    """Base class for all database models."""


class DBWallet(Base):
    """Database model for a wallet."""

    __tablename__ = "wallets"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    address: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    expected_quantity: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String)
