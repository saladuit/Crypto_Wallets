""" "Tests for wallet-related API routes."""


def test_create_wallet_success(client):
    """Test creating a wallet successfully."""
    payload = {"address": "0x123", "expected_quantity": 1.23, "currency": "ETH"}
    resp = client.post("/api/wallets/", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["address"] == payload["address"]
    assert float(data["expected_quantity"]) == payload["expected_quantity"]
    assert data["currency"] == payload["currency"]
    assert "id" in data


def test_create_wallet_conflict(client, wallet_factory):
    """Test creating a wallet with a conflicting address."""
    w = wallet_factory(address="0xconflict")
    payload = {"address": w.address, "expected_quantity": 0.0, "currency": "ETH"}
    resp = client.post("/api/wallets/", json=payload)
    assert resp.status_code == 409


def test_read_wallet_found(client, wallet_factory):
    """Test reading an existing wallet."""
    w = wallet_factory(address="0xreadme", expected_quantity=9.0, currency="BTC")
    resp = client.get(f"/api/wallets/{w.id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == w.id
    assert data["address"] == w.address


def test_read_wallet_not_found(client):
    """Test reading a non-existing wallet."""
    resp = client.get("/api/wallets/99999")
    assert resp.status_code == 404


def test_delete_wallet(client, wallet_factory):
    """Test deleting an existing wallet."""
    w = wallet_factory(address="0xdelme")
    resp = client.delete(f"/api/wallets/{w.id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == w.id

    resp2 = client.get(f"/api/wallets/{w.id}")
    assert resp2.status_code == 404


def test_delete_nonexistent_wallet(client):
    """Test deleting an nonexistent wallet."""
    resp = client.delete("/api/wallets/99999")
    assert resp.status_code == 404


def test_update_wallet_noop(client, wallet_factory):
    """Test updating an existing wallet (no-op)."""
    w = wallet_factory(address="0xupd")
    resp = client.put(f"/api/wallets/{w.id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == w.id


def test_update_nonexistent_wallet_noop(client):
    """Test updating an existing wallet (no-op)."""
    resp = client.put("/api/wallets/99999")
    assert resp.status_code == 404