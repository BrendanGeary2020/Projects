from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_admin_and_customer_cannot_share_same_id():

    user_id = 900020

    admin = {
        "id": user_id,
        "name": "Test Admin",
        "email": "testadmin900020@example.com",
        "username": "admin900020"
    }

    admin_response = client.post(
        "/admins/",
        json=admin
    )

    assert admin_response.status_code == 201

    customer = {
        "id": user_id,
        "name": "Test Customer",
        "email": "testcustomer900020@example.com",
        "username": "customer900020"
    }

    customer_response = client.post(
        "/customers/",
        json=customer
    )

    assert customer_response.status_code == 400

    # Clean up
    delete_response = client.delete(
        f"/admins/{user_id}"
    )

    assert delete_response.status_code == 200


def test_customer_and_admin_cannot_share_same_id():

    user_id = 900021

    customer = {
        "id": user_id,
        "name": "Test Customer",
        "email": "testcustomer900021@example.com",
        "username": "customer900021"
    }

    customer_response = client.post(
        "/customers/",
        json=customer
    )

    assert customer_response.status_code == 201

    admin = {
        "id": user_id,
        "name": "Test Admin",
        "email": "testadmin900021@example.com",
        "username": "admin900021"
    }

    admin_response = client.post(
        "/admins/",
        json=admin
    )

    assert admin_response.status_code == 400

    # Clean up
    delete_response = client.delete(
        f"/customers/{user_id}"
    )

    assert delete_response.status_code == 200


def test_duplicate_customer_id_is_rejected():

    user_id = 900022

    customer = {
        "id": user_id,
        "name": "First Customer",
        "email": "first900022@example.com",
        "username": "customer900022"
    }

    first_response = client.post(
        "/customers/",
        json=customer
    )

    assert first_response.status_code == 201

    duplicate_customer = {
        "id": user_id,
        "name": "Second Customer",
        "email": "second900022@example.com",
        "username": "customer900022second"
    }

    second_response = client.post(
        "/customers/",
        json=duplicate_customer
    )

    assert second_response.status_code == 400

    # Clean up
    delete_response = client.delete(
        f"/customers/{user_id}"
    )

    assert delete_response.status_code == 200


def test_duplicate_admin_id_is_rejected():

    user_id = 900023

    admin = {
        "id": user_id,
        "name": "First Admin",
        "email": "first900023@example.com",
        "username": "admin900023"
    }

    first_response = client.post(
        "/admins/",
        json=admin
    )

    assert first_response.status_code == 201

    duplicate_admin = {
        "id": user_id,
        "name": "Second Admin",
        "email": "second900023@example.com",
        "username": "admin900023second"
    }

    second_response = client.post(
        "/admins/",
        json=duplicate_admin
    )

    assert second_response.status_code == 400

    # Clean up
    delete_response = client.delete(
        f"/admins/{user_id}"
    )

    assert delete_response.status_code == 200