""" "CRUD operations for Wallet model."""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from backend.models.wallet import Wallet, WalletCreate
from backend.db.wallet import DBWallet


def db_find_wallet(wallet_id: int, db: Session) -> DBWallet:
    """Helper function to find a wallet by ID or raise NotFoundError."""
    db_wallet = db.query(DBWallet).filter(DBWallet.id == wallet_id).first()
    return db_wallet


def db_create_wallet(wallet: WalletCreate, session: Session) -> Wallet:
    """Create a new wallet in the database."""
    db_wallet = DBWallet(**wallet.model_dump())
    session.add(db_wallet)
    try:
        session.commit()
        session.refresh(db_wallet)
    except IntegrityError:
        session.rollback()
        return None
    return Wallet(**db_wallet.__dict__)


def db_read_wallet(wallet_id: int, session: Session) -> Wallet:
    """Read a wallet from the database by its ID."""
    db_wallet = db_find_wallet(wallet_id, session)
    if db_wallet is None:
        return None
    return Wallet(**db_wallet.__dict__)


def db_update_wallet(wallet_id: int, session: Session) -> Wallet:
    """Update a wallet in the database by its ID."""
    db_wallet = db_find_wallet(wallet_id, session)
    if db_wallet is None:
        return None
    for key, value in db_wallet.__dict__.items():
        setattr(db_wallet, key, value)

    session.commit()
    session.refresh(db_wallet)

    return Wallet(**db_wallet.__dict__)


def db_delete_wallet(wallet_id: int, session: Session) -> Wallet:
    """Delete a wallet from the database by its ID."""
    db_wallet = db_find_wallet(wallet_id, session)
    if db_wallet is None:
        return None
    session.delete(db_wallet)
    session.commit()
    return Wallet(**db_wallet.__dict__)
