import pytest
from unittest.mock import MagicMock, patch

from src.domain.exceptions import EmptyReviewError
from src.application.read_model.review_read_model import ReviewReadModel

class TestGetAllReviews:
    def test_returns_list(self, client):
        read_model = ReviewReadModel(
            review_id=1,
            place_id=2,
            user_id=3,
            content_in="Дужи добри",
        )
        with patch("src.presentation.control_review.GetAllReviewsHandler") as MockHandler:
            MockHandler.return_value.handle.return_value = [read_model]
            resp = client.get("/review/all")

        assert resp.status_code == 200
        assert resp.json()[0]["content_in"] == "Дужи добри"

    def test_empty_list(self, client):
        with patch("src.presentation.control_review.GetAllReviewsHandler") as MockHandler:
            MockHandler.return_value.handle.return_value = []
            resp = client.get("/review/all")

        assert resp.status_code == 200
        assert resp.json() == []

    def test_multiple_reviews_returned(self, client):
        reviews = [
            ReviewReadModel(review_id=i, place_id=1, user_id=1, content_in=f"Відгук {i}")
            for i in range(5)
        ]
        with patch("src.presentation.control_review.GetAllReviewsHandler") as MockHandler:
            MockHandler.return_value.handle.return_value = reviews
            resp = client.get("/review/all")
 
        assert len(resp.json()) == 5

class TestCreateReview:
    def test_success_returns_201(self, client):
        with patch("src.presentation.control_review.CreateReviewHandler") as MockHandler:
            MockHandler.return_value.handle.return_value = 5
            resp = client.post(
                "/review/create",
                params={"place_id": 1, "content_in": "Прекрасно"},
            )

        assert resp.status_code == 201
        assert resp.json()["review_id"] == 5

    def test_empty_content_returns_400(self, client):
        with patch("src.presentation.control_review.CreateReviewHandler") as MockHandler:
            MockHandler.return_value.handle.side_effect = EmptyReviewError()
            resp = client.post(
                "/review/create",
                params={"place_id": 1, "content_in": ""},
            )
 
        assert resp.status_code == 400

    def test_missing_place_id_returns_422(self, client):
        resp = client.post("/review/create", params={"content_in": "Непогано"})
        assert resp.status_code == 422
 
    def test_handler_uses_current_user_id(self, client):
        with patch("src.presentation.control_review.CreateReviewHandler") as MockHandler:
            MockHandler.return_value.handle.return_value = 1
            client.post(
                "/review/create",
                params={"place_id": 3, "content_in": "Тест"},
            )
 
        command = MockHandler.return_value.handle.call_args[0][0]
        assert command.user_id == 1
        assert command.place_id == 3
        assert command.content_in == "Тест"


class TestDeleteReview:
    def test_success_returns_200(self, client):
        with patch("src.presentation.control_review.DeleteReviewHandler") as MockHandler:
            MockHandler.return_value.handle.return_value = None
            resp = client.delete("/review/1")
 
        assert resp.status_code == 200
        assert "message" in resp.json()

    def test_delete_calls_handler_with_correct_id(self, client):
        with patch("src.presentation.control_review.DeleteReviewHandler") as MockHandler:
            MockHandler.return_value.handle.return_value = None
            client.delete("/review/77")

        command = MockHandler.return_value.handle.call_args[0][0]
        assert command.review_id == 77
