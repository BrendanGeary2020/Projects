from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_get_admins():

    response = client.get("/admins/")

    assert response.status_code == 200


def test_get_admin():

    response = client.get("/admins/1")

    assert response.status_code == 200


def test_get_admin_not_found():

    response = client.get("/admins/99999")

    assert response.status_code == 404

def test_create_admin():

    new_admin = {
        "id": 999,
        "name": "Test Admin",
        "email": "testadmin@example.com"
    }

    response = client.post(
        "/admins/",
        json=new_admin
    )

    assert response.status_code == 201

    # Clean up test data
    delete_response = client.delete("/admins/999")

    assert delete_response.status_code == 200

def test_update_admin():

    new_admin = {
        "id": 1000,
        "name": "Update Test Admin",
        "email": "update@example.com"
    }

    # Create test admin
    create_response = client.post(
        "/admins/",
        json=new_admin
    )

    assert create_response.status_code == 201

    # Update admin
    updated_admin = {
        "id": 1000,
        "name": "Updated Admin",
        "email": "updated@example.com"
    }

    update_response = client.put(
        "/admins/1000",
        json=updated_admin
    )

    assert update_response.status_code == 200

    # Verify updated name
    assert update_response.json()["name"] == "Updated Admin"

    # Clean up
    delete_response = client.delete("/admins/1000")

    assert delete_response.status_code == 200

def test_delete_admin():

    new_admin = {
        "id": 1001,
        "name": "Delete Test Admin",
        "email": "deleteadmin@example.com"
    }

    # Create test admin
    create_response = client.post(
        "/admins/",
        json=new_admin
    )

    assert create_response.status_code == 201

    # Delete admin
    delete_response = client.delete("/admins/1001")

    assert delete_response.status_code == 200

    # Verify admin no longer exists
    get_response = client.get("/admins/1001")

    assert get_response.status_code == 404

def test_create_duplicate_admin():

    new_admin = {
        "id": 1005,
        "name": "Duplicate Test Admin",
        "email": "duplicate@example.com"
    }

    # Create first admin
    first_response = client.post(
        "/admins/",
        json=new_admin
    )

    assert first_response.status_code == 201

    # Try to create the same admin again
    second_response = client.post(
        "/admins/",
        json=new_admin
    )

    assert second_response.status_code == 400

    # Clean up
    delete_response = client.delete("/admins/1005")

    assert delete_response.status_code == 200

def test_create_duplicate_customer():

    new_customer = {
        "id": 1005,
        "name": "Duplicate Test Customer",
        "email": "duplicatecustomer@example.com",
        "department": "IT",
        "salary": 50000
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
    delete_response = client.delete("/customers/1005")

    assert delete_response.status_code == 200

def test_update_admin_not_found():

    updated_admin = {
        "id": 9998,
        "name": "Does Not Exist",
        "email": "notfound@example.com"
    }

    response = client.put(
        "/admins/9998",
        json=updated_admin
    )

    assert response.status_code == 404

def test_delete_admin_not_found():

    response = client.delete("/admins/9998")

    assert response.status_code == 404