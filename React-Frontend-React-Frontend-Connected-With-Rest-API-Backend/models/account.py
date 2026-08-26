from pydantic import BaseModel, Field

from typing import Literal


AccountType = Literal[
    "checking",
    "savings"
]


class AccountCreate(BaseModel):

    customer_id: int
    account_type: AccountType
    balance: float = Field(ge=0)

class AccountCreate(BaseModel):

    customer_id: int

    account_type: AccountType

    balance: float = Field(
        ge=0
    )


class DepositRequest(BaseModel):

    amount: float = Field(
        gt=0
    )


class WithdrawalRequest(BaseModel):

    amount: float = Field(
        gt=0
    )