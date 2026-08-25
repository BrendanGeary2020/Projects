from database.mongodb import customers_collection
from models.customer import Customer


def get_customers(
    department: str | None = None,
    search: str | None = None
):

    query = {}

    # Filter by department
    if department:
        query["department"] = {
            "$regex": f"^{department}$",
            "$options": "i"
        }

    # Search by customer name
    if search:
        query["name"] = {
            "$regex": search,
            "$options": "i"
        }

    return list(
        customers_collection.find(
            query,
            {"_id": 0}
        )
    )


def get_customer(customer_id: int):

    return customers_collection.find_one(
        {"id": customer_id},
        {"_id": 0}
    )


def create_customer(customer: Customer):

    customers_collection.insert_one(
        customer.model_dump()
    )

    return customer


def update_customer(
    customer_id: int,
    updated_customer: Customer
):

    result = customers_collection.update_one(
        {"id": customer_id},
        {"$set": updated_customer.model_dump()}
    )

    return result


def delete_customer(customer_id: int):

    customer = customers_collection.find_one(
        {"id": customer_id},
        {"_id": 0}
    )

    if customer:
        customers_collection.delete_one(
            {"id": customer_id}
        )

    return customer