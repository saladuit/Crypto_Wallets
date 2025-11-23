"""Module defining FastAPI routes for wallet operations."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from backend.crud.wallet import (
    db_create_wallet,
    db_read_wallet,
    db_update_wallet,
    db_delete_wallet,
)
from backend.db.wallet import DBWallet
from backend.models.wallet import Wallet, WalletCreate, WalletUpdate
from backend.db.get_db import get_db
from backend.services.external_wallets import get_external_wallets


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


@router.get("/compare")
def compare_wallets(db: Session = Depends(get_db)):
    """Compare local wallets in the DB against the mocked external API.

    Returns a list of comparison objects for each unique address found in
    either source. Each item contains the address, local quantity,
    external quantity, currencies and a boolean `match` indicating whether
    the quantities are equal (only meaningful when both sides are present).
    """
    db_wallets = db.query(DBWallet).all()
    local_map = {w.address: w for w in db_wallets}

    external_wallets = get_external_wallets()
    external_map = {w["address"]: w for w in external_wallets}

    addresses = set(local_map.keys()) | set(external_map.keys())

    results = []
    for addr in sorted(addresses):
        local = local_map.get(addr)
        ext = external_map.get(addr)

        local_qty = float(local.expected_quantity) if local is not None else None
        ext_qty = float(ext.get("quantity")) if ext is not None else None

        status = None
        difference = None
        if local is not None and ext is not None:
            difference = (
                round(ext_qty - local_qty, 12)
                if (
                    isinstance(ext_qty, (int, float))
                    and isinstance(local_qty, (int, float))
                )
                else None
            )
            status = "match" if local_qty == ext_qty else "mismatch"
        elif local is not None and ext is None:
            status = "external_not_found"
        else:
            status = "local_not_found"

        results.append(
            {
                "address": addr,
                "local_quantity": local_qty,
                "local_currency": local.currency if local is not None else None,
                "external_quantity": ext_qty,
                "external_currency": ext.get("currency") if ext is not None else None,
                "status": status,
                "difference": difference,
            }
        )

    return results


@router.get("/{wallet_id}")
def read_wallet(wallet_id: int, db: Session = Depends(get_db)) -> Wallet:
    """Read a wallet by its ID."""
    db_wallet = db_read_wallet(wallet_id, db)
    if db_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return db_wallet


@router.put("/{wallet_id}")
def update_wallet(
    wallet_id: int, wallet: WalletUpdate, db: Session = Depends(get_db)
) -> Wallet:
    """Update a wallet by its ID."""
    db_wallet = db_update_wallet(wallet_id, wallet, db)
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
