from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_get_customers():

    response = client.get("/customers/")

    assert response.status_code == 200


def test_get_customer():

    customer = {
        "id": 900001,
        "name": "Get Test Customer",
        "email": "getcustomer@example.com",
        "username": "getcustomer"
    }

    create_response = client.post(
        "/customers/",
        json=customer
    )

    assert create_response.status_code == 201

    response = client.get("/customers/900001")

    assert response.status_code == 200
    assert response.json()["id"] == 900001

    delete_response = client.delete("/customers/900001")

    assert delete_response.status_code == 200


def test_get_customer_not_found():

    response = client.get("/customers/999999")

    assert response.status_code == 404


def test_create_customer():

    new_customer = {
        "id": 900002,
        "name": "Test Customer",
        "email": "testcustomer@example.com",
        "username": "testcustomer"
    }

    response = client.post(
        "/customers/",
        json=new_customer
    )

    assert response.status_code == 201

    assert response.json()["id"] == 900002
    assert response.json()["name"] == "Test Customer"
    assert response.json()["email"] == "testcustomer@example.com"
    assert response.json()["username"] == "testcustomer"

    # Clean up
    delete_response = client.delete("/customers/900002")

    assert delete_response.status_code == 200


def test_update_customer():

    new_customer = {
        "id": 900003,
        "name": "Update Test Customer",
        "email": "updatecustomer@example.com",
        "username": "updatecustomer"
    }

    # Create test customer
    create_response = client.post(
        "/customers/",
        json=new_customer
    )

    assert create_response.status_code == 201

    # Update customer
    updated_customer = {
        "id": 900003,
        "name": "Updated Customer",
        "email": "updatedcustomer@example.com",
        "username": "updatedcustomer"
    }

    update_response = client.put(
        "/customers/900003",
        json=updated_customer
    )

    assert update_response.status_code == 200

    # Verify updated values
    assert update_response.json()["name"] == "Updated Customer"
    assert update_response.json()["email"] == "updatedcustomer@example.com"
    assert update_response.json()["username"] == "updatedcustomer"

    # Clean up
    delete_response = client.delete("/customers/900003")

    assert delete_response.status_code == 200


def test_delete_customer():

    new_customer = {
        "id": 900004,
        "name": "Delete Test Customer",
        "email": "deletecustomer@example.com",
        "username": "deletecustomer"
    }

    # Create test customer
    create_response = client.post(
        "/customers/",
        json=new_customer
    )

    assert create_response.status_code == 201

    # Delete customer
    delete_response = client.delete("/customers/900004")

    assert delete_response.status_code == 200

    # Verify customer no longer exists
    get_response = client.get("/customers/900004")

    assert get_response.status_code == 404


def test_create_duplicate_customer():

    new_customer = {
        "id": 900005,
        "name": "Duplicate Test Customer",
        "email": "duplicate@example.com",
        "username": "duplicatecustomer"
    }

    # Create first customer
    first_response = client.post(
        "/customers/",
        json=new_customer
    )

    assert first_response.status_code == 201

    # Try to create the same customer again
    second_response = client.post(
        "/customers/",
        json=new_customer
    )

    assert second_response.status_code == 400

    # Clean up
    delete_response = client.delete("/customers/900005")

    assert delete_response.status_code == 200


def test_update_customer_not_found():

    updated_customer = {
        "id": 999998,
        "name": "Does Not Exist",
        "email": "notfound@example.com",
        "username": "notfound"
    }

    response = client.put(
        "/customers/999998",
        json=updated_customer
    )

    assert response.status_code == 404


def test_delete_customer_not_found():

    response = client.delete("/customers/999999")

    assert response.status_code == 404