from fastapi.testclient import TestClient
from src.app.app import app, get_repo
import pytest
import asyncio

class FakeRepo():
    def __init__(self):
        self.orders = [{"id": 1, "title": 
                        "Тестовый заказ", "status": 
                        "new"}]

    async def get_all(self):
        return self.orders

    async def delete(self, order_id: int):
        for i, order in enumerate(self
.orders):
            if order["id"] == order_id:
                del self.orders[i]
                return True
        return False

    async def get_by_id(self, order_id: int):
        for order in self.orders:
            if order["id"] == order_id:
                return order
        return None

    async def get_all_limit(self, limit: int):
        return self.orders[:limit]

    async def update_status(self, order_id: int, new_status: str):
        for order in self.orders:
            if order["id"] == order_id:
                order["status"] = new_status
                return True
        return False

@pytest.fixture
def client():
  fakerepo = FakeRepo()
  app.dependency_overrides[get_repo] = lambda: fakerepo
  client = TestClient(app)

  yield client
  app.dependency_overrides.clear()

def test_get_html(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"]

def test_get_orders(client):
    response = client.get("/orders")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Тестовый заказ"
    assert response.headers["content-type"]

def test_invalid_order(client):
    response = client.get("/orders/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Данного заказа не существует"

def test_invalid_limit(client):
    response = client.get("/order/limit/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Невозможный лимит"

def test_delete_order(client):
    response = client.delete("/delete_order/1")
    assert response.status_code == 200
    assert response.json()["success"] is True
    response = client.get("/orders")
    assert len(response.json()) == 0

def test_update_order(client):
    response = client.patch("/update_order/1", json={"status": "done"})
    assert response.status_code == 200
    assert response.json()["success"] is True
    response = client.get("/orders")
    assert response.json()[0]["status"] == "done"
