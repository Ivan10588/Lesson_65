from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_and_get_item():
    payload = {
        "name": "Test Item",
        "price": 10.5,
        "tax": 1.0
    }
    r = client.post("/items/", json=payload)
    assert r.status_code == 201
    data = r.json()
    item_id = data["id"]

    r2 = client.get(f"/items/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["name"] == "Test Item"

def test_search_items():
    r = client.post("/items/", json={"name": "Shovel", "price": 500.0})
    assert r.status_code == 201
    r_search = client.get("/items/search/?q=shovel")
    assert r_search.status_code == 200
    items = r_search.json()
    assert len(items) >= 1
    assert any(item["name"].lower().find("shovel") != -1 for item in items)

def test_validation_price_zero():
    r = client.post("/items/", json={
        "name": "Bad Item",
        "price": 0,
    })
    assert r.status_code == 422
