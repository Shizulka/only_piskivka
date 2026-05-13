import os
import sys
import unittest.mock as _mock

os.environ.setdefault("KEY", "horse")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("DB_USER", "test")
os.environ.setdefault("DB_PASSWORD", "test")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DB_NAME", "test_db")

_mock.patch("sqlalchemy.create_engine", return_value=_mock.MagicMock()).start()
_mock.patch("sqlalchemy.MetaData.create_all", return_value=None).start()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from unittest.mock import MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.presentation import control_place, control_user, control_review
from src.infrastructure.database import get_db
from src.infrastructure.dependencies import get_current_user

_app = FastAPI()
_app.include_router(control_place.router)
_app.include_router(control_user.router)
_app.include_router(control_review.router)


def _make_mock_user(user_id=1):
    u = MagicMock()
    u.user_id = user_id
    u.user_name = "степан"
    u.email = "stepan@yahoo.com"
    u.is_admin = False
    return u


@pytest.fixture
def client():
    mock_db = MagicMock()
    _app.dependency_overrides[get_db] = lambda: mock_db
    _app.dependency_overrides[get_current_user] = lambda: _make_mock_user()
    with TestClient(_app) as c:
        yield c
    _app.dependency_overrides.clear()
