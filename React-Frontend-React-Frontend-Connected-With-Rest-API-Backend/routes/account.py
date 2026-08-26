from fastapi import APIRouter

from models.account import (
    AccountCreate,
    DepositRequest,
    WithdrawalRequest
)

from services.account_service import (
    get_accounts,
    get_account,
    create_account,
    delete_account,
    deposit,
    withdraw,
    add_interest
)


router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)


@router.get("/")
def read_accounts():
    return get_accounts()


@router.get("/{account_id}")
def read_account(account_id: int):

    from fastapi import HTTPException

    account = get_account(account_id)

    if not account:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    return account


@router.post("/", status_code=201)
def add_account(account: AccountCreate):

    return create_account(account)


@router.delete("/{account_id}")
def remove_account(account_id: int):

    return delete_account(account_id)


@router.post("/{account_id}/deposit")
def make_deposit(
    account_id: int,
    request: DepositRequest
):

    return deposit(
        account_id,
        request.amount
    )


@router.post("/{account_id}/withdraw")
def make_withdrawal(
    account_id: int,
    request: WithdrawalRequest
):

    return withdraw(
        account_id,
        request.amount
    )


@router.post("/{account_id}/interest")
def apply_interest(account_id: int):

    return add_interest(account_id)