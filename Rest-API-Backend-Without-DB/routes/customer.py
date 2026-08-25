from fastapi import APIRouter, HTTPException

from models.customer import Customer

from services.customer_service import (
    get_customers,
    get_customer,
    create_customer,
    update_customer,
    delete_customer
)


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


# GET - Get all customers / filter / search
@router.get("/")
def get_all_customers(
    department: str | None = None,
    search: str | None = None
):

    return get_customers(
        department,
        search
    )


# GET - Get one customer
@router.get("/{customer_id}")
def get_one_customer(customer_id: int):

    customer = get_customer(customer_id)

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


# POST - Create customer
@router.post("/", status_code=201)
def create_new_customer(customer: Customer):

    existing_customer = get_customer(customer.id)

    if existing_customer:
        raise HTTPException(
            status_code=400,
            detail="Customer ID already exists"
        )

    return create_customer(customer)


# PUT - Update customer
@router.put("/{customer_id}")
def update_existing_customer(
    customer_id: int,
    updated_customer: Customer
):

    result = update_customer(
        customer_id,
        updated_customer
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return updated_customer


# DELETE - Delete customer
@router.delete("/{customer_id}")
def delete_existing_customer(customer_id: int):

    customer = delete_customer(customer_id)

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer