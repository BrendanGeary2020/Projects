from fastapi import APIRouter, HTTPException

from models.customer import Customer
from services.customer_service import (
    get_customers,
    get_customer,
    create_customer,
    update_customer,
    delete_customer
)

from services.account_service import (
    get_customer_accounts
)


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.get("/")
def read_customers():
    return get_customers()


@router.get("/{customer_id}")
def read_customer(customer_id: int):

    customer = get_customer(customer_id)

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


@router.get("/{customer_id}/accounts")
def read_customer_accounts(customer_id: int):

    customer = get_customer(customer_id)

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return get_customer_accounts(customer_id)


@router.post("/", status_code=201)
def add_customer(customer: Customer):

    result = create_customer(customer)

    if not result:
        raise HTTPException(
            status_code=400,
            detail="Customer ID already exists"
        )

    return result


@router.put("/{customer_id}")
def edit_customer(
    customer_id: int,
    customer: Customer
):

    result = update_customer(
        customer_id,
        customer
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return result


@router.delete("/{customer_id}")
def remove_customer(customer_id: int):

    result = delete_customer(customer_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return result