import pytest
from unittest.mock import MagicMock, patch

from src.domain.exceptions import EmptyReviewError

class TestGetAllReviews:
    def test_returns_list(self, client):
        mock_review = MagicMock()
        mock_review.review_id = 1
        mock_review.place_id = 2
        mock_review.user_id = 3
        mock_review.content_in = "Дужи добри"

        with patch("src.presentation.control_review.ReviewService") as MockSvc:
            MockSvc.return_value.all_review.return_value = [mock_review]
            resp = client.get("/review/all")

        assert resp.status_code == 200
        assert resp.json()[0]["content_in"] == "Дужи добри"

    def test_empty_list(self, client):
        with patch("src.presentation.control_review.ReviewService") as MockSvc:
            MockSvc.return_value.all_review.return_value = []
            resp = client.get("/review/all")

        assert resp.status_code == 200
        assert resp.json() == []

class TestCreateReview:
    def test_success(self, client):
        mock_review = MagicMock()
        mock_review.review_id = 5
        mock_review.place_id = 1
        mock_review.user_id = 1
        mock_review.content_in = "Прекрасно"

        with patch("src.presentation.control_review.ReviewService") as MockSvc:
            MockSvc.return_value.create_review.return_value = mock_review
            resp = client.post("/review/create", params={"place_id": 1, "content_in": "Прекрасно"})

        assert resp.status_code == 200
        assert resp.json()["content_in"] == "Прекрасно"

    def test_empty_content_returns_400(self, client):
        with patch("src.presentation.control_review.ReviewService") as MockSvc:
            MockSvc.return_value.create_review.side_effect = EmptyReviewError()
            resp = client.post("/review/create", params={"place_id": 1, "content_in": ""})

        assert resp.status_code == 400

class TestDeleteReview:
    def test_success(self, client):
        with patch("src.presentation.control_review.ReviewService") as MockSvc:
            MockSvc.return_value.delete_review.return_value = True
            resp = client.delete("/review/1")

        assert resp.status_code == 200

    def test_not_found_returns_404(self, client):
        with patch("src.presentation.control_review.ReviewService") as MockSvc:
            MockSvc.return_value.delete_review.return_value = False
            resp = client.delete("/review/999")

        assert resp.status_code == 404
