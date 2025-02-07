from fastapi.testclient import TestClient
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
