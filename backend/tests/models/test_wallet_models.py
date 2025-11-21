import pytest
from pydantic import ValidationError

from backend.models.wallet import Wallet, WalletCreate, WalletUpdate


def test_wallet_model_serialization_and_types():
    """Test that Wallet model serializes correctly and types are as expected."""
    w = Wallet(id=1, address="0xabc", expected_quantity=1.5, currency="ETH")
    data = w.model_dump()

    assert data["id"] == 1
    assert data["address"] == "0xabc"
    assert isinstance(data["expected_quantity"], float)
    assert data["currency"] == "ETH"


def test_wallet_missing_required_field_raises():
    """Test that Wallet model raises ValidationError when required fields are missing."""
    with pytest.raises(ValidationError):
        Wallet(address="0xabc", expected_quantity=1.0, currency="ETH")


def test_walletcreate_coercion_and_validation():
    """Test that WalletCreate model coerces types correctly."""
    wc = WalletCreate(address="0xdef", expected_quantity="2", currency="BTC")
    d = wc.model_dump()
    assert isinstance(d["expected_quantity"], float)
    assert d["expected_quantity"] == 2.0


def test_walletupdate_requires_expected_quantity():
    """Test that WalletUpdate model raises ValidationError when expected_quantity is missing."""
    with pytest.raises(ValidationError):
        WalletUpdate()
