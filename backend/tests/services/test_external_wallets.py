"""Tests for the mocked external wallets service."""

from backend.services.external_wallets import get_external_wallets


def test_get_external_wallets_shape_and_values():
    """Test the shape and expected values of the mocked external wallets."""
    data = get_external_wallets()
    assert isinstance(data, list)
    assert len(data) == 3

    # expected hard-coded values
    expected = {
        "0xExternalAddr1": {"quantity": 10.0, "currency": "ETH"},
        "0xExternalAddr2": {"quantity": 5.5, "currency": "BTC"},
        "0xExternalAddr3": {"quantity": 0.0, "currency": "USDT"},
    }

    for item in data:
        # basic shape
        assert (
            "address" in item
            and "quantity" in item
            and "currency" in item
            and "id" in item
        )
        assert isinstance(item["address"], str)
        assert isinstance(item["quantity"], (int, float))
        assert isinstance(item["currency"], str)

        # expected values
        assert item["address"] in expected
        exp = expected[item["address"]]
        assert float(item["quantity"]) == exp["quantity"]
        assert item["currency"] == exp["currency"]
