from fastapi.testclient import TestClient
from full_project.main import app, items_db

client = TestClient(app)


def test_create_item():
    response = client.post("/items", json={
        "title": "Book",
        "description": "Fantasy"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Book"
    assert "id" in data


def test_get_items():
    items_db.clear()  # очистка перед тестом
    # создаём пару элементов
    client.post("/items", json={"title": "A"})
    client.post("/items", json={"title": "B"})
    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_item():
    items_db.clear()
    response = client.post("/items", json={"title": "Old"})
    item_id = response.json()["id"]
    response = client.put(f"/items/{item_id}", json={"title": "New"})
    assert response.json()["title"] == "New"


def test_delete_item():
    items_db.clear()
    response = client.post("/items", json={"title": "DeleteMe"})
    item_id = response.json()["id"]
    response = client.delete(f"/items/{item_id}")
    assert response.json()["status"] == "deleted"
