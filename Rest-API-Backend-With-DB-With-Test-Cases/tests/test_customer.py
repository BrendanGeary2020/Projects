from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_get_customers():

    response = client.get("/customers/")

    assert response.status_code == 200
    
def test_get_customer():

    response = client.get("/customers/1")

    assert response.status_code == 200

def test_get_customer_not_found():

    response = client.get("/customers/99999")

    assert response.status_code == 404

def test_create_customer():

    new_customer = {
        "id": 999,
        "name": "Test Customer",
        "email": "testcustomer@example.com",
        "department": "IT",
        "salary": 50000
    }

    response = client.post(
        "/customers/",
        json=new_customer
    )

    assert response.status_code == 201

    # Clean up test data
    delete_response = client.delete("/customers/999")

    assert delete_response.status_code == 200

def test_update_customer():

    new_customer = {
        "id": 1000,
        "name": "Update Test Customer",
        "email": "updatecustomer@example.com",
        "department": "IT",
        "salary": 50000
    }

    # Create test customer
    create_response = client.post(
        "/customers/",
        json=new_customer
    )

    assert create_response.status_code == 201

    # Update customer
    updated_customer = {
        "id": 1000,
        "name": "Updated Customer",
        "email": "updatedcustomer@example.com",
        "department": "HR",
        "salary": 60000
    }

    update_response = client.put(
        "/customers/1000",
        json=updated_customer
    )

    assert update_response.status_code == 200

    # Verify updated values
    assert update_response.json()["name"] == "Updated Customer"
    assert update_response.json()["department"] == "HR"
    assert update_response.json()["salary"] == 60000

    # Clean up
    delete_response = client.delete("/customers/1000")

    assert delete_response.status_code == 200

def test_delete_customer():

    new_customer = {
        "id": 1001,
        "name": "Delete Test Customer",
        "email": "deletecustomer@example.com",
        "department": "IT",
        "salary": 50000
    }

    # Create test customer
    create_response = client.post(
        "/customers/",
        json=new_customer
    )

    assert create_response.status_code == 201

    # Delete customer
    delete_response = client.delete("/customers/1001")

    assert delete_response.status_code == 200

    # Verify customer no longer exists
    get_response = client.get("/customers/1001")

    assert get_response.status_code == 404

def test_customer_department_filter():

    new_customer = {
        "id": 1002,
        "name": "Filter Test Customer",
        "email": "filter@example.com",
        "department": "IT",
        "salary": 50000
    }

    # Create test customer
    create_response = client.post(
        "/customers/",
        json=new_customer
    )

    assert create_response.status_code == 201

    # Search using lowercase "it"
    response = client.get(
        "/customers/?department=it"
    )

    assert response.status_code == 200

    customers = response.json()

    assert any(
        customer["id"] == 1002
        for customer in customers
    )

    # Clean up
    delete_response = client.delete("/customers/1002")

    assert delete_response.status_code == 200

def test_customer_name_search():

    new_customer = {
        "id": 1003,
        "name": "Search Test Customer",
        "email": "search@example.com",
        "department": "IT",
        "salary": 50000
    }

    # Create test customer
    create_response = client.post(
        "/customers/",
        json=new_customer
    )

    assert create_response.status_code == 201

    # Search using lowercase "search"
    response = client.get(
        "/customers/?search=search"
    )

    assert response.status_code == 200

    customers = response.json()

    assert any(
        customer["id"] == 1003
        for customer in customers
    )

    # Clean up
    delete_response = client.delete("/customers/1003")

    assert delete_response.status_code == 200

def test_customer_department_and_search():

    new_customer = {
        "id": 1004,
        "name": "John Filter Customer",
        "email": "johnfilter@example.com",
        "department": "IT",
        "salary": 55000
    }

    # Create test customer
    create_response = client.post(
        "/customers/",
        json=new_customer
    )

    assert create_response.status_code == 201

    # Filter by department and search by name
    response = client.get(
        "/customers/?department=it&search=john"
    )

    assert response.status_code == 200

    customers = response.json()

    assert any(
        customer["id"] == 1004
        for customer in customers
    )

    # Clean up
    delete_response = client.delete("/customers/1004")

    assert delete_response.status_code == 200

def test_update_customer_not_found():

    updated_customer = {
        "id": 9998,
        "name": "Does Not Exist",
        "email": "notfound@example.com",
        "department": "IT",
        "salary": 50000
    }

    response = client.put(
        "/customers/9998",
        json=updated_customer
    )

    assert response.status_code == 404

def test_delete_customer_not_found():

    response = client.delete("/customers/9998")

    assert response.status_code == 404