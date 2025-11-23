"""Tests for the /wallets/compare endpoint."""

from typing import Dict


def _make_ext(addr: str, qty: float, cur: str) -> Dict:
    """Helper to create an external wallet dict."""
    return {"id": 0, "address": addr, "quantity": qty, "currency": cur}


def test_compare_match(client, wallet_factory, monkeypatch):
    """Test the /wallets/compare endpoint for matching quantities."""
    wallet_factory(address="0xmatch", expected_quantity=10.0, currency="ETH")

    def _mock():
        return [_make_ext("0xmatch", 10.0, "ETH")]

    monkeypatch.setattr("backend.routes.wallets.get_external_wallets", _mock)

    resp = client.get("/wallets/compare")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    m = {item["address"]: item for item in data}
    assert "0xmatch" in m
    item = m["0xmatch"]
    assert item["status"] == "match"
    assert float(item["difference"]) == 0.0


def test_compare_mismatch(client, wallet_factory, monkeypatch):
    """Test the /wallets/compare endpoint for mismatching quantities."""
    wallet_factory(address="0xmismatch", expected_quantity=5.0, currency="BTC")

    def _mock():
        return [_make_ext("0xmismatch", 7.5, "BTC")]

    monkeypatch.setattr("backend.routes.wallets.get_external_wallets", _mock)

    resp = client.get("/wallets/compare")
    assert resp.status_code == 200
    data = resp.json()
    m = {item["address"]: item for item in data}
    item = m["0xmismatch"]
    assert item["status"] == "mismatch"
    assert abs(float(item["difference"]) - 2.5) < 1e-9


def test_compare_external_not_found(client, wallet_factory, monkeypatch):
    """Test the /wallets/compare endpoint when local wallet exists but no external wallet."""
    wallet_factory(address="0xnoext", expected_quantity=1.0, currency="USDT")

    def _mock():
        return []

    monkeypatch.setattr("backend.routes.wallets.get_external_wallets", _mock)

    resp = client.get("/wallets/compare")
    assert resp.status_code == 200
    data = resp.json()
    m = {item["address"]: item for item in data}
    item = m["0xnoext"]
    assert item["status"] == "external_not_found"
    assert item["difference"] is None


def test_compare_local_not_found(client, monkeypatch):
    """Test the /wallets/compare endpoint when external wallet exists but no local wallet."""

    def _mock():
        return [_make_ext("0xexternalOnly", 3.14, "ETH")]

    monkeypatch.setattr("backend.routes.wallets.get_external_wallets", _mock)

    resp = client.get("/wallets/compare")
    assert resp.status_code == 200
    data = resp.json()
    m = {item["address"]: item for item in data}
    assert "0xexternalOnly" in m
    item = m["0xexternalOnly"]
    assert item["status"] == "local_not_found"
    assert item["difference"] is None

    assert float(item["external_quantity"]) == 3.14
    assert item["external_currency"] == "ETH"
    assert item["local_quantity"] is None
    assert item["local_currency"] is None
