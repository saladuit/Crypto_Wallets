"""Tests for the main app endpoints."""


def test_health_check(client):
    """Health check endpoint should return status ok."""
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
