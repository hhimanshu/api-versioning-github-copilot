import pytest
from fastapi.testclient import TestClient
from ..app import app

client = TestClient(app)

def test_hello_endpoint():
    """Test the hello endpoint returns expected response"""
    response = client.get("/hello")
    
    # Verify status code
    assert response.status_code == 200
    
    # Verify response content
    assert response.json() == {"message": "Hello, World!"}
    
    # Verify content type
    assert response.headers["content-type"] == "application/json"

@pytest.mark.asyncio
async def test_hello_endpoint_async():
    """Test the hello endpoint asynchronously"""
    response = client.get("/hello")
    assert response.status_code == 200
