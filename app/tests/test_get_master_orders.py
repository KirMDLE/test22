from fastapi.testclient import TestClient
from app.main import app  
from app.database import SessionLocal
from app import models
import pytest

client = TestClient(app)

@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_get_master_orders(db_session):
    order1 = models.Order(client_id=10, master_id=1, /* другие поля */)
    order2 = models.Order(client_id=11, master_id=1, /* другие поля */)
    db_session.add_all([order1, order2])
    db_session.commit()

    response = client.get("/master/1")
    assert response.status_code == 200

    orders = response.json()
    assert isinstance(orders, list)
    assert len(orders) == 2
    assert all(order["master_id"] == 1 for order in orders)
