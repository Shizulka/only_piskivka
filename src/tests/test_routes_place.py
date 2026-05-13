import pytest
from datetime import time
from unittest.mock import MagicMock, patch

from src.domain.exceptions import InvalidTimeRangeError

class TestGetAllPlaces:
    def test_returns_list(self, client):
        mock_place = MagicMock()
        mock_place.place_id = 1
        mock_place.location = "Вул. Привокзальна, 21"
        mock_place.working_hours.open_time = time(11, 0)
        mock_place.working_hours.close_time = time(19, 0)
        mock_place.status = "bar"

        with patch("src.presentation.control_place.PlaceService") as MockSvc:
            MockSvc.return_value.all_places.return_value = [mock_place]
            resp = client.get("/place/all")

        assert resp.status_code == 200
        assert resp.json()[0]["location"] == "Вул. Привокзальна, 21"

    def test_empty_list(self, client):
        with patch("src.presentation.control_place.PlaceService") as MockSvc:
            MockSvc.return_value.all_places.return_value = []
            resp = client.get("/place/all")

        assert resp.status_code == 200
        assert resp.json() == []

class TestCreatePlace:
    def test_success(self, client):
        mock_place = MagicMock()
        mock_place.place_id = 10
        mock_place.location = "Вул. Філіпова, 12"
        mock_place.working_hours.open_time = "07:30"
        mock_place.working_hours.close_time = "19:30"
        mock_place.status = "cafe"

        with patch("src.presentation.control_place.PlaceService") as MockSvc:
            MockSvc.return_value.create_place.return_value = mock_place
            resp = client.post(
                "/place/create",
                params={"location": "Вул. Філіпова, 12", "open": "07:30:00", "close": "19:30:00", "place_status": "cafe"},
            )

        assert resp.status_code == 200
        assert resp.json()["place_id"] == 10

    def test_invalid_hours_returns_400(self, client):
        with patch("src.presentation.control_place.PlaceService") as MockSvc:
            MockSvc.return_value.create_place.side_effect = InvalidTimeRangeError()
            resp = client.post(
                "/place/create",
                params={"location": "десь", "open": "22:00:00", "close": "08:00:00", "place_status": "cafe"},
            )

        assert resp.status_code == 400

class TestDeletePlace:
    def test_success(self, client):
        with patch("src.presentation.control_place.PlaceService") as MockSvc:
            MockSvc.return_value.delete_place.return_value = True
            resp = client.delete("/place/1")

        assert resp.status_code == 200

    def test_not_found_returns_404(self, client):
        with patch("src.presentation.control_place.PlaceService") as MockSvc:
            MockSvc.return_value.delete_place.return_value = False
            resp = client.delete("/place/999")

        assert resp.status_code == 404
