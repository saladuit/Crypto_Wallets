from backend.db.get_db import get_db

import backend.db.get_db as db_module


def test_get_db_yields_and_closes(monkeypatch):
    """Verify get_db yields a session and calls its close() on generator close."""

    closed = {"called": False}

    class DummySession:
        """A dummy session that tracks if close() is called."""
        def close(self):
            """Mark that close was called."""
            closed["called"] = True

    monkeypatch.setattr(db_module, "SessionLocal", DummySession)

    gen = get_db()
    session = next(gen)

    assert isinstance(session, DummySession)

    gen.close()
    assert closed["called"] is True
