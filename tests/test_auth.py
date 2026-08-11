from datetime import timedelta

from quizzable.services import auth


def test_create_and_verify_access_token_roundtrip():
    token = auth.create_access_token({"sub": "alice"})
    verified, data = auth.verify_access_token(token)
    assert verified is True
    assert data["sub"] == "alice"


def test_verify_rejects_expired_token():
    token = auth.create_access_token({"sub": "bob"}, timedelta(minutes=-1))
    verified, _ = auth.verify_access_token(token)
    assert verified is False


def test_verify_rejects_garbage_token():
    assert auth.verify_access_token("not-a-real-token") == (False, {})


def test_verify_strips_exp_from_returned_data():
    token = auth.create_access_token({"sub": "carol"})
    _, data = auth.verify_access_token(token)
    assert "exp" not in data
