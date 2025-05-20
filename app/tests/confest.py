from fastapi.testclient import TestClient
from app.main import app  
import pytest

@pytest.fixture
def client():
    return TestClient(app)

def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200