import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException

from src.modules.core.infrastructure.dependencies import get_current_user, get_current_admin_user
from src.modules.core.infrastructure.database import get_db, db_ping

class TestGetDb:
    def test_yields_session_and_closes(self):
        mock_session = MagicMock()
        mock_session_local = MagicMock(return_value=mock_session)

        with patch("src.modules.core.infrastructure.database.SessionLocal", mock_session_local):
            gen = get_db()
            session = next(gen)
            assert session is mock_session

            try:
                next(gen)
            except StopIteration:
                pass

        mock_session.close.assert_called_once()

    def test_session_closed_even_on_exception(self):
        mock_session = MagicMock()
        mock_session_local = MagicMock(return_value=mock_session)

        with patch("src.modules.core.infrastructure.database.SessionLocal", mock_session_local):
            gen = get_db()
            next(gen)
            with pytest.raises(RuntimeError, match="boom"):
                gen.throw(RuntimeError("boom"))

        mock_session.close.assert_called_once()

class TestDbPing:
    def test_executes_select_1(self):
        db = MagicMock()
        db_ping(db)
        db.execute.assert_called_once()
        call_arg = db.execute.call_args[0][0]
        assert "SELECT 1" in str(call_arg)

class TestGetCurrentUser:
    def _make_token(self, user_id=1):
        import jwt
        from datetime import datetime, timedelta, timezone
        payload = {"sub": str(user_id), "exp": datetime.now(timezone.utc) + timedelta(minutes=10)}
        return jwt.encode(payload, "horse", algorithm="HS256")

    def _call(self, token, mock_user=None):
        mock_db = MagicMock()
        with patch("src.modules.core.infrastructure.dependencies.UserRepository") as MockRepo:
            MockRepo.return_value.get_user_by_id.return_value = mock_user
            return get_current_user(token=token, db=mock_db)

    def test_valid_token_returns_user(self):
        mock_user = MagicMock()
        mock_user.user_id = 1
        token = self._make_token(user_id=1)
        result = self._call(token, mock_user=mock_user)
        assert result is mock_user

    def test_invalid_token_raises_401(self):
        with pytest.raises(HTTPException) as exc_info:
            self._call("not.a.valid.token")
        assert exc_info.value.status_code == 401

    def test_user_not_found_raises_401(self):
        token = self._make_token(user_id=999)
        with pytest.raises(HTTPException) as exc_info:
            self._call(token, mock_user=None)
        assert exc_info.value.status_code == 401

    def test_token_missing_sub_raises_401(self):
        import jwt
        from datetime import datetime, timedelta, timezone
        payload = {"exp": datetime.now(timezone.utc) + timedelta(minutes=10)}
        token = jwt.encode(payload, "horse", algorithm="HS256")
        with pytest.raises(HTTPException) as exc_info:
            self._call(token)
        assert exc_info.value.status_code == 401

    def test_expired_token_raises_401(self):
        import jwt
        from datetime import datetime, timedelta, timezone
        payload = {"sub": "1", "exp": datetime.now(timezone.utc) - timedelta(minutes=1)}
        token = jwt.encode(payload, "horse", algorithm="HS256")
        with pytest.raises(HTTPException) as exc_info:
            self._call(token)
        assert exc_info.value.status_code == 401

    def test_wrong_key_raises_401(self):
        import jwt
        from datetime import datetime, timedelta, timezone
        payload = {"sub": "1", "exp": datetime.now(timezone.utc) + timedelta(minutes=10)}
        token = jwt.encode(payload, "wrong_key", algorithm="HS256")
        with pytest.raises(HTTPException) as exc_info:
            self._call(token)
        assert exc_info.value.status_code == 401

class TestGetCurrentAdminUser:
    def test_admin_user_passes(self):
        admin = MagicMock()
        admin.is_admin = True
        result = get_current_admin_user(current_user=admin)
        assert result is admin

    def test_non_admin_raises_403(self):
        user = MagicMock()
        user.is_admin = False
        with pytest.raises(HTTPException) as exc_info:
            get_current_admin_user(current_user=user)
        assert exc_info.value.status_code == 403

    def test_403_error_message(self):
        user = MagicMock()
        user.is_admin = False
        with pytest.raises(HTTPException) as exc_info:
            get_current_admin_user(current_user=user)
        assert "permission" in exc_info.value.detail.lower() or "Insufficient" in exc_info.value.detail