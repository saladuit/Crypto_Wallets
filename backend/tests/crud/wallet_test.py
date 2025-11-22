"""Tests for CRUD operations on Wallet model."""
from backend.models.wallet import WalletCreate, WalletUpdate
from backend.crud.wallet import (
    db_find_wallet,
    db_create_wallet,
    db_read_wallet,
    db_update_wallet,
    db_delete_wallet,
)


class TestCrudWallet:
    """Tests for CRUD operations on Wallet model."""
    def test_db_find_wallet_not_found(self, db_session):
        """Test finding a wallet that does not exist."""
        wallet = db_find_wallet(1, db_session)
        assert wallet is None

    def test_db_create_wallet(self, db_session):
        """Test creating a new wallet."""
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
        """Test creating a wallet that already exists (should fail)."""
        w = wallet_factory(address="0xabc")
        wallet_in = WalletCreate(
            address=w.address,
            expected_quantity=2.0,
            currency="ETH",
        )
        created = db_create_wallet(wallet_in, db_session)
        assert created is None

    def test_db_wallet_read(self, db_session, wallet_factory):
        """Test reading a wallet from the database."""
        w = wallet_factory(address="0xdef", expected_quantity=2.0, currency="BTC")

        read = db_read_wallet(w.id, db_session)
        assert read.address == w.address
        assert read.expected_quantity == w.expected_quantity
        assert read.currency == w.currency

    def test_db_update_wallet(self, db_session, wallet_factory):
        """Test updating a wallet in the database."""
        w = wallet_factory(address="0xdef", expected_quantity=2.0, currency="BTC")

        # perform a no-op update by passing the same expected_quantity
        update_payload = WalletUpdate(expected_quantity=w.expected_quantity)
        updated = db_update_wallet(w.id, update_payload, db_session)
        assert updated.id == w.id
        assert updated.address == w.address
        assert updated.expected_quantity == w.expected_quantity
        assert updated.currency == w.currency

    def test_db_update_wallet_invalid_string_input(self, db_session, wallet_factory):
        """Invalid string input for expected_quantity should leave value unchanged."""
        w = wallet_factory(address="0xbadstr", expected_quantity=2.5, currency="ETH")

        # use a lightweight object with an attribute that bypasses Pydantic validation
        update_payload = type("BadPayload", (), {"expected_quantity": "not-a-number"})()
        updated = db_update_wallet(w.id, update_payload, db_session)
        assert updated is not None
        assert updated.expected_quantity == w.expected_quantity

    def test_db_update_wallet_invalid_none_input(self, db_session, wallet_factory):
        """None for expected_quantity should be treated as no-op and leave value unchanged."""
        w = wallet_factory(address="0xbadnone", expected_quantity=7.5, currency="BTC")

        update_payload = type("BadPayload", (), {"expected_quantity": None})()
        updated = db_update_wallet(w.id, update_payload, db_session)
        assert updated is not None
        assert updated.expected_quantity == w.expected_quantity

    def test_db_update_wallet_missing_attribute(self, db_session, wallet_factory):
        """If the update payload lacks expected_quantity attribute, no update occurs."""
        w = wallet_factory(address="0xnoattr", expected_quantity=4.2, currency="USD")

        # plain object has no expected_quantity attribute
        update_payload = object()
        updated = db_update_wallet(w.id, update_payload, db_session)
        assert updated is not None
        assert updated.expected_quantity == w.expected_quantity

    def test_db_delete_wallet(self, db_session, wallet_factory):
        """Test deleting a wallet from the database."""
        w = wallet_factory(address="0x123", expected_quantity=0.0, currency="USD")

        deleted = db_delete_wallet(w.id, db_session)
        assert deleted.id == w.id
        assert deleted.address == w.address

        wallet = db_find_wallet(w.id, db_session)
        assert wallet is None
