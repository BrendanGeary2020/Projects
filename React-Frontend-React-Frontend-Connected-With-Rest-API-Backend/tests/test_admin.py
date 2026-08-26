from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_get_admins():

    response = client.get("/admins/")

    assert response.status_code == 200


def test_get_admin():

    admin = {
        "id": 900010,
        "name": "Get Test Admin",
        "email": "getadmin@example.com",
        "username": "getadmin"
    }

    create_response = client.post(
        "/admins/",
        json=admin
    )

    assert create_response.status_code == 201

    response = client.get("/admins/900010")

    assert response.status_code == 200
    assert response.json()["id"] == 900010

    # Clean up
    delete_response = client.delete("/admins/900010")

    assert delete_response.status_code == 200


def test_get_admin_not_found():

    response = client.get("/admins/999999")

    assert response.status_code == 404


def test_create_admin():

    new_admin = {
        "id": 900011,
        "name": "Test Admin",
        "email": "testadmin@example.com",
        "username": "testadmin"
    }

    response = client.post(
        "/admins/",
        json=new_admin
    )

    assert response.status_code == 201

    assert response.json()["id"] == 900011
    assert response.json()["name"] == "Test Admin"
    assert response.json()["email"] == "testadmin@example.com"
    assert response.json()["username"] == "testadmin"

    # Clean up
    delete_response = client.delete("/admins/900011")

    assert delete_response.status_code == 200


def test_update_admin():

    new_admin = {
        "id": 900012,
        "name": "Update Test Admin",
        "email": "update@example.com",
        "username": "updateadmin"
    }

    # Create test admin
    create_response = client.post(
        "/admins/",
        json=new_admin
    )

    assert create_response.status_code == 201

    # Update admin
    updated_admin = {
        "id": 900012,
        "name": "Updated Admin",
        "email": "updated@example.com",
        "username": "updatedadmin"
    }

    update_response = client.put(
        "/admins/900012",
        json=updated_admin
    )

    assert update_response.status_code == 200

    # Verify updated values
    assert update_response.json()["name"] == "Updated Admin"
    assert update_response.json()["email"] == "updated@example.com"
    assert update_response.json()["username"] == "updatedadmin"

    # Clean up
    delete_response = client.delete("/admins/900012")

    assert delete_response.status_code == 200


def test_delete_admin():

    new_admin = {
        "id": 900013,
        "name": "Delete Test Admin",
        "email": "deleteadmin@example.com",
        "username": "deleteadmin"
    }

    # Create test admin
    create_response = client.post(
        "/admins/",
        json=new_admin
    )

    assert create_response.status_code == 201

    # Delete admin
    delete_response = client.delete("/admins/900013")

    assert delete_response.status_code == 200

    # Verify admin no longer exists
    get_response = client.get("/admins/900013")

    assert get_response.status_code == 404


def test_create_duplicate_admin():

    new_admin = {
        "id": 900014,
        "name": "Duplicate Test Admin",
        "email": "duplicate@example.com",
        "username": "duplicateadmin"
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
    delete_response = client.delete("/admins/900014")

    assert delete_response.status_code == 200


def test_update_admin_not_found():

    updated_admin = {
        "id": 999998,
        "name": "Does Not Exist",
        "email": "notfound@example.com",
        "username": "notfoundadmin"
    }

    response = client.put(
        "/admins/999998",
        json=updated_admin
    )

    assert response.status_code == 404


def test_delete_admin_not_found():

    response = client.delete("/admins/999999")

    assert response.status_code == 404