# test_masters.py
#     pytest app/tests/test_masters.py

from fastapi.testclient import TestClient
from app.main import app  
import pytest

client = TestClient(app)

def test_get_all_masters():
    response = client.get("/masters/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
