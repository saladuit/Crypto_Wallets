import pytest

from backend.models.wallet import WalletCreate
from backend.crud.wallet import (
    db_find_wallet,
    db_create_wallet,
    db_read_wallet,
    db_update_wallet,
    db_delete_wallet,
)


class TestCrudWallet:
    def test_db_find_wallet_not_found(self, db_session):
        wallet = db_find_wallet(1, db_session)
        assert wallet is None

    def test_db_create_wallet(self, db_session):
        wallet_in = WalletCreate(
            address="0xabc",
            expected_quantity=1.5,
            currency="ETH",
        )
        created = db_create_wallet(wallet_in, db_session)
        assert created.address == wallet_in.address
        assert created.expected_quantity == wallet_in.expected_quantity
        assert created.currency == wallet_in.currency
    
    def test_db_create_existing_wallet(self, db_session, wallet_factory):
        w = wallet_factory(address="0xabc")
        wallet_in = WalletCreate(
            address=w.address,
            expected_quantity=2.0,
            currency="ETH",
        )
        created = db_create_wallet(wallet_in, db_session)
        assert created is None

    def test_db_wallet_read(self, db_session, wallet_factory):
        w = wallet_factory(address="0xdef", expected_quantity=2.0, currency="BTC")

        read = db_read_wallet(w.id, db_session)
        assert read.address == w.address
        assert read.expected_quantity == w.expected_quantity
        assert read.currency == w.currency

    def test_db_update_wallet(self, db_session, wallet_factory):
        w = wallet_factory(address="0xdef", expected_quantity=2.0, currency="BTC")

        updated = db_update_wallet(w.id, db_session)
        assert updated.id == w.id
        assert updated.address == w.address
        assert updated.expected_quantity == w.expected_quantity
        assert updated.currency == w.currency

    def test_db_delete_wallet(self, db_session, wallet_factory):
        w = wallet_factory(address="0x123", expected_quantity=0.0, currency="USD")

        deleted = db_delete_wallet(w.id, db_session)
        assert deleted.id == w.id
        assert deleted.address == w.address

        wallet = db_find_wallet(w.id, db_session)
        assert wallet is None