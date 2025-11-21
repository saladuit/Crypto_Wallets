import pytest
from sqlalchemy.exc import IntegrityError

from backend.db.wallet import DBWallet


class TestDBWallet:
    def test_insert_and_query(self, db_session):
        w = DBWallet(address="0x1", expected_quantity=1.23, currency="ETH")
        db_session.add(w)
        db_session.commit()
        db_session.refresh(w)

        assert w.id is not None
        found = db_session.query(DBWallet).filter_by(id=w.id).one()
        assert found.address == "0x1"
        assert found.expected_quantity == 1.23
        assert found.currency == "ETH"

    def test_unique_address_constraint(self, db_session):
        w1 = DBWallet(address="0xdup", expected_quantity=0.0, currency="BTC")
        db_session.add(w1)
        db_session.commit()

        w2 = DBWallet(address="0xdup", expected_quantity=5.0, currency="BTC")
        db_session.add(w2)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_address_non_nullable(self, db_session):
        # If address is defined NOT NULL in mapping, inserting None should fail
        w = DBWallet(address=None, expected_quantity=0.0, currency="ETH")
        db_session.add(w)
        with pytest.raises(IntegrityError):
            db_session.commit()
