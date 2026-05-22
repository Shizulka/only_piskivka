import pytest
from unittest.mock import MagicMock, patch, AsyncMock

from src.modules.core.domain.exceptions import InvalidTimeRangeError
from src.modules.core.application.read_model.place_read_model import PlaceReadModel

class TestGetAllPlaces:
    def test_returns_list(self, client):
        read_model = PlaceReadModel(
            id=1,
            location="Вул. Привокзальна, 21",
            open_time="11:00",
            close_time="19:00",
            status="bar",
        )
        with patch("src.modules.core.presentation.control_place.GetAllPlacesHandler") as MockHandler:
            MockHandler.return_value.handle.return_value = [read_model]
            resp = client.get("/place/all")

        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["location"] == "Вул. Привокзальна, 21"
        assert data[0]["id"] == 1

    def test_empty_list(self, client):
        with patch("src.modules.core.presentation.control_place.GetAllPlacesHandler") as MockHandler:
            MockHandler.return_value.handle.return_value = []
            resp = client.get("/place/all")

        assert resp.status_code == 200
        assert resp.json() == []

    def test_multiple_places_returned(self, client):
        places = [
            PlaceReadModel(id=i, location=f"Вул. {i}", open_time="10:00", close_time="20:00", status="bar")
            for i in range(3)
        ]
        with patch("src.modules.core.presentation.control_place.GetAllPlacesHandler") as MockHandler:
            MockHandler.return_value.handle.return_value = places
            resp = client.get("/place/all")

        assert resp.status_code == 200
        assert len(resp.json()) == 3

    def test_no_auth_required(self, client):
        with patch("src.modules.core.presentation.control_place.GetAllPlacesHandler") as MockHandler:
            MockHandler.return_value.handle.return_value = []
            resp = client.get("/place/all")
        assert resp.status_code == 200

class TestCreatePlace:
    def test_success_returns_201(self, admin_client):
        with patch("src.modules.core.presentation.control_place.CreatePlaceHandler") as MockHandler:
            MockHandler.return_value.handle = AsyncMock(return_value=10)
            resp = admin_client.post(
                "/place/create",
                params={
                    "location": "Вул. Філіпова, 12",
                    "open_time": "07:30:00",
                    "close_time": "19:30:00",
                    "place_status": "cafe",
                },
            )

        assert resp.status_code == 201
        assert resp.json()["place_id"] == 10
        assert "message" in resp.json()

    def test_invalid_hours_returns_400(self, admin_client):
        with patch("src.modules.core.presentation.control_place.CreatePlaceHandler") as MockHandler:
            MockHandler.return_value.handle = AsyncMock(side_effect=InvalidTimeRangeError())
            resp = admin_client.post(
                "/place/create",
                params={
                    "location": "десь",
                    "open_time": "22:00:00",
                    "close_time": "08:00:00",
                    "place_status": "cafe",
                },
            )

        assert resp.status_code == 400

    def test_missing_location_returns_422(self, admin_client):
        resp = admin_client.post(
            "/place/create",
            params={"open_time": "09:00:00", "close_time": "18:00:00", "place_status": "bar"},
        )
        assert resp.status_code == 422

    def test_non_admin_returns_403(self, client):
        resp = client.post(
            "/place/create",
            params={
                "location": "Вул. Соборна, 67",
                "open_time": "09:00:00",
                "close_time": "18:00:00",
                "place_status": "bar",
            },
        )
        assert resp.status_code == 403

    def test_handler_receives_correct_command(self, admin_client):
        with patch("src.modules.core.presentation.control_place.CreatePlaceHandler") as MockHandler:
            MockHandler.return_value.handle = AsyncMock(return_value=1)
            admin_client.post(
                "/place/create",
                params={
                    "location": "Вул. Сіркова, 167",
                    "open_time": "08:00:00",
                    "close_time": "20:00:00",
                    "place_status": "shop",
                },
            )

        command = MockHandler.return_value.handle.call_args[0][0]
        assert command.location == "Вул. Сіркова, 167"
        assert command.status == "shop"

class TestDeletePlace:
    def test_success_returns_200(self, admin_client):
        with patch("src.modules.core.presentation.control_place.DeletePlaceHandler") as MockHandler:
            MockHandler.return_value.handle = AsyncMock(return_value=None)
            resp = admin_client.delete("/place/1")

        assert resp.status_code == 200
        assert "message" in resp.json()

    def test_non_admin_returns_403(self, client):
        resp = client.delete("/place/1")
        assert resp.status_code == 403

    def test_delete_calls_handler_with_correct_id(self, admin_client):
        with patch("src.modules.core.presentation.control_place.DeletePlaceHandler") as MockHandler:
            MockHandler.return_value.handle = AsyncMock(return_value=None)
            admin_client.delete("/place/42")

        command = MockHandler.return_value.handle.call_args[0][0]
        assert command.place_id == 42
