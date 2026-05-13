import os
import pytest
from unittest.mock import patch

class TestPasswordHashing:
    def test_hash_and_verify_correct(self):
        with patch("src.security.get_password_hash.pwd_context") as mock_ctx:
            mock_ctx.hash.return_value = "$2b$12$fakehash"
            mock_ctx.verify.side_effect = lambda plain, _: plain == "mypassword"

            from src.security.get_password_hash import get_password_hash, verify_password
            hashed = get_password_hash("mypassword")
            assert hashed == "$2b$12$fakehash"
            assert verify_password("mypassword", hashed) is True

    def test_verify_wrong_password(self):
        with patch("src.security.get_password_hash.pwd_context") as mock_ctx:
            mock_ctx.verify.side_effect = lambda plain, _: plain == "mypassword"

            from src.security.get_password_hash import verify_password
            assert verify_password("wrongpassword", "$2b$12$fakehash") is False

class TestJWT:
    def test_create_access_token_is_string(self):
        from src.security.get_password_hash import create_access_token
        token = create_access_token({"sub": "42"})
        assert isinstance(token, str)

    def test_token_contains_correct_subject(self):
        import jwt as pyjwt
        from src.security.get_password_hash import create_access_token
        token = create_access_token({"sub": "42"})
        decoded = pyjwt.decode(token, os.environ["KEY"], algorithms=[os.environ["ALGORITHM"]])
        assert decoded["sub"] == "42"

    def test_token_contains_expiry(self):
        import jwt as pyjwt
        from src.security.get_password_hash import create_access_token
        token = create_access_token({"sub": "1"})
        decoded = pyjwt.decode(token, os.environ["KEY"], algorithms=[os.environ["ALGORITHM"]])
        assert "exp" in decoded
