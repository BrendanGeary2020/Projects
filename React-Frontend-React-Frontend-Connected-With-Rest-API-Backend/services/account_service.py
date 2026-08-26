from fastapi import HTTPException

from database.mongodb import (
    accounts_collection,
    users_collection
)


CHECKING_INTEREST_RATE = 0.02
SAVINGS_INTEREST_RATE = 0.03


def get_accounts():

    return list(
        accounts_collection.find(
            {},
            {"_id": 0}
        )
    )


def get_account(account_id: int):

    return accounts_collection.find_one(
        {"id": account_id},
        {"_id": 0}
    )


def get_customer_accounts(customer_id: int):

    return list(
        accounts_collection.find(
            {"customer_id": customer_id},
            {"_id": 0}
        )
    )


def get_next_account_id():

    accounts = accounts_collection.find(
        {},
        {
            "_id": 0,
            "id": 1
        }
    )

    existing_ids = set()

    for account in accounts:

        if "id" in account:

            try:
                existing_ids.add(
                    int(account["id"])
                )

            except (TypeError, ValueError):
                continue

    next_id = 1

    while next_id in existing_ids:
        next_id += 1

    return next_id


def create_account(account):

    # Check that the customer exists

    customer = users_collection.find_one(
        {
            "id": account.customer_id,
            "user_type": "customer"
        }
    )

    if not customer:

        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )


    # Only one checking account or one savings
    # account is allowed per customer

    existing_type = accounts_collection.find_one(
        {
            "customer_id": account.customer_id,
            "account_type": account.account_type
        }
    )
    if existing_type:
        return {
            "success": False,
            "message": (
                f"Customer already has a "
                f"{account.account_type} account"
            )
        }
    # if existing_type:

    #     raise HTTPException(
    #         status_code=400,
    #         detail=(
    #             f"Customer already has a "
    #             f"{account.account_type} account"
    #         )
    #     )


    # Find the first available account ID

    new_account_id = get_next_account_id()


    # Create the account

    new_account = {
        "id": new_account_id,
        "customer_id": account.customer_id,
        "account_type": account.account_type,
        "balance": account.balance
    }


    # Extra safety check in case the ID
    # somehow already exists

    if accounts_collection.find_one(
        {"id": new_account_id}
    ):

        raise HTTPException(
            status_code=500,
            detail="Could not generate a unique account ID"
        )


    # Save the account

    accounts_collection.insert_one(
        new_account
    )


    # Retrieve it without MongoDB's _id

    saved_account = accounts_collection.find_one(
        {"id": new_account_id},
        {"_id": 0}
    )


    return saved_account


def delete_account(account_id: int):

    account = get_account(account_id)

    if not account:

        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )


    accounts_collection.delete_one(
        {"id": account_id}
    )


    return account


def deposit(
    account_id: int,
    amount: float
):

    account = get_account(account_id)

    if not account:

        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )


    if amount <= 0:

        raise HTTPException(
            status_code=400,
            detail="Deposit amount must be greater than zero"
        )


    new_balance = (
        account["balance"] + amount
    )


    accounts_collection.update_one(
        {"id": account_id},
        {
            "$set": {
                "balance": new_balance
            }
        }
    )


    return get_account(account_id)


def withdraw(
    account_id: int,
    amount: float
):

    account = get_account(account_id)

    if not account:

        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )


    if amount <= 0:

        raise HTTPException(
            status_code=400,
            detail="Withdrawal amount must be greater than zero"
        )


    if amount > account["balance"]:

        raise HTTPException(
            status_code=400,
            detail="Insufficient funds"
        )


    new_balance = (
        account["balance"] - amount
    )


    accounts_collection.update_one(
        {"id": account_id},
        {
            "$set": {
                "balance": new_balance
            }
        }
    )


    return get_account(account_id)


def add_interest(account_id: int):

    account = get_account(account_id)

    if not account:

        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )


    if account["account_type"] == "checking":

        interest_rate = CHECKING_INTEREST_RATE

    elif account["account_type"] == "savings":

        interest_rate = SAVINGS_INTEREST_RATE

    else:

        raise HTTPException(
            status_code=400,
            detail="Invalid account type"
        )


    new_balance = (
        account["balance"]
        + (
            account["balance"]
            * interest_rate
        )
    )


    accounts_collection.update_one(
        {"id": account_id},
        {
            "$set": {
                "balance": new_balance
            }
        }
    )


    return get_account(account_id)