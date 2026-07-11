def test_product_crud_and_search(client):
    response = client.post(
        "/products",
        json={
            "name": "USB Keyboard",
            "description": "Wired keyboard",
            "category": "Accessories",
            "unit_price": "199.99",
            "available_quantity": 10,
        },
    )
    assert response.status_code == 201
    product_id = response.json()["id"]

    response = client.get("/products", params={"search": "keyboard"})
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = client.put(f"/products/{product_id}", json={"available_quantity": 12})
    assert response.status_code == 200
    assert response.json()["available_quantity"] == 12

    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 204

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 404


def test_customer_duplicate_email_validation(client):
    payload = {
        "full_name": "Amina Jacobs",
        "email": "amina@example.com",
        "phone_number": "+27115550123",
    }
    assert client.post("/customers", json=payload).status_code == 201

    response = client.post("/customers", json=payload)
    assert response.status_code == 409
    assert response.json()["detail"] == "Customer email already exists"


def test_order_lifecycle_updates_and_restores_stock(client):
    customer = client.post(
        "/customers",
        json={
            "full_name": "Neo Mokoena",
            "email": "neo@example.com",
            "phone_number": "+27825550123",
        },
    ).json()
    product = client.post(
        "/products",
        json={
            "name": "Laptop Stand",
            "description": "Adjustable aluminium stand",
            "category": "Office",
            "unit_price": "350.00",
            "available_quantity": 5,
        },
    ).json()

    response = client.post(
        "/orders",
        json={"customer_id": customer["id"], "items": [{"product_id": product["id"], "quantity": 2}]},
    )
    assert response.status_code == 201
    order = response.json()
    assert order["status"] == "CREATED"
    assert order["total_amount"] in ("700.00", 700.0, "700")

    product_after_order = client.get(f"/products/{product['id']}").json()
    assert product_after_order["available_quantity"] == 3

    response = client.post(
        "/orders",
        json={"customer_id": customer["id"], "items": [{"product_id": product["id"], "quantity": 10}]},
    )
    assert response.status_code == 400

    response = client.patch(f"/orders/{order['id']}/cancel")
    assert response.status_code == 200
    assert response.json()["status"] == "CANCELLED"

    product_after_cancel = client.get(f"/products/{product['id']}").json()
    assert product_after_cancel["available_quantity"] == 5


def test_validation_errors(client):
    response = client.post(
        "/products",
        json={
            "name": "",
            "description": "Bad product",
            "category": "General",
            "unit_price": "-1.00",
            "available_quantity": -2,
        },
    )
    assert response.status_code == 422

    response = client.post(
        "/customers",
        json={"full_name": "Bad Email", "email": "not-an-email", "phone_number": "12"},
    )
    assert response.status_code == 422

    response = client.post("/orders", json={"customer_id": 999, "items": [{"product_id": 1, "quantity": 1}]})
    assert response.status_code == 404
