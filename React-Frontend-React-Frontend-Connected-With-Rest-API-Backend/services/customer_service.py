from database.mongodb import users_collection, accounts_collection


def get_customers():
    return list(
        users_collection.find(
            {"user_type": "customer"},
            {"_id": 0}
        )
    )


def get_customer(customer_id: int):
    return users_collection.find_one(
        {
            "id": customer_id,
            "user_type": "customer"
        },
        {"_id": 0}
    )


def create_customer(customer):

    existing_user = users_collection.find_one(
        {"id": customer.id}
    )

    if existing_user:
        return None

    customer_data = customer.model_dump()

    customer_data["user_type"] = "customer"

    users_collection.insert_one(
        customer_data
    )

    return customer


def update_customer(
    customer_id: int,
    updated_customer
):

    existing_customer = get_customer(customer_id)

    if not existing_customer:
        return None

    updated_data = updated_customer.model_dump()

    updated_data["user_type"] = "customer"

    users_collection.update_one(
        {
            "id": customer_id,
            "user_type": "customer"
        },
        {
            "$set": updated_data
        }
    )

    return updated_customer


def delete_customer(customer_id: int):

    customer = get_customer(customer_id)

    if not customer:
        return None

    users_collection.delete_one(
        {
            "id": customer_id,
            "user_type": "customer"
        }
    )

    # Delete customer's accounts as well.
    accounts_collection.delete_many(
        {"customer_id": customer_id}
    )

    return customer