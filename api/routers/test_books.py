from fastapi.testclient import TestClient

from services.api_version import ApiVersion
from ..app import app

client = TestClient(app)


def test_create_valid_book(create_book_model):
    book_data = create_book_model.model_dump(mode='json')
    response = client.post("/books/", json=book_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == create_book_model.title
    assert data["author"] == create_book_model.author
    assert "_id" in data


def test_invalid_api_version(create_book_model):
    book_data = create_book_model.model_dump(mode='json')
    response = client.post(
        "/books/",
        json=book_data,
        headers={"X-API-Version": "invalid-version"}
    )

    assert response.status_code == 400
    error_detail = response.json()
    assert "Invalid version:" in error_detail["detail"]
    valid_versions = error_detail["valid_versions"]
    assert len(valid_versions) >= 2
    assert ApiVersion.LATEST.value in valid_versions


def test_deprecated_api_version(create_book_model):
    book_data = create_book_model.model_dump(mode='json')
    response = client.post(
        "/books/",
        json=book_data,
        headers={"X-API-Version": ApiVersion.V2024_07_16.value}
    )

    assert response.status_code == 410
    error_detail = response.json()
    assert "deprecated" in error_detail["detail"]
    assert "sunset" in error_detail["detail"]