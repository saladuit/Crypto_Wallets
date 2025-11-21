"""Module defining FastAPI routes for wallet operations."""

from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session

from backend.crud.wallet import (
    db_create_wallet,
    db_read_wallet,
    db_update_wallet,
    db_delete_wallet,
)
from backend.db.wallet import DBWallet
from backend.models.wallet import Wallet, WalletCreate
from backend.db.get_db import get_db


router = APIRouter(prefix="/wallets", tags=["wallets"])


@router.post("/")
def create_wallet(wallet: WalletCreate, db: Session = Depends(get_db)) -> Wallet:
    """Create a new wallet."""
    existing_wallet = (
        db.query(DBWallet).filter(DBWallet.address == wallet.address).first()
    )
    if existing_wallet:
        raise HTTPException(status_code=409, detail="Wallet already exists")
    return db_create_wallet(wallet, db)


@router.get("/", response_model=List[Wallet])
def list_wallets(db: Session = Depends(get_db)) -> List[Wallet]:
    """List all wallets.

    This returns a simple list view for the collection endpoint so GET
    against `/wallets` (or `/api/wallets` if you mount the router under
    `/api`) works from the frontend and curl.
    """
    db_wallets = db.query(DBWallet).all()
    return [
        Wallet(
            id=w.id,
            address=w.address,
            expected_quantity=w.expected_quantity,
            currency=w.currency,
        )
        for w in db_wallets
    ]


@router.get("/{wallet_id}")
def read_wallet(wallet_id: int, db: Session = Depends(get_db)) -> Wallet:
    """Read a wallet by its ID."""
    db_wallet = db_read_wallet(wallet_id, db)
    if db_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return db_wallet


@router.put("/{wallet_id}")
def update_wallet(wallet_id: int, db: Session = Depends(get_db)) -> Wallet:
    """Update a wallet by its ID."""
    db_wallet = db_update_wallet(wallet_id, db)
    if db_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return db_wallet


@router.delete("/{wallet_id}")
def delete_wallet(wallet_id: int, db: Session = Depends(get_db)) -> Wallet:
    """Delete a wallet by its ID."""
    db_wallet = db_delete_wallet(wallet_id, db)
    if db_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return db_wallet
