from pydantic import BaseModel, Field
from decimal import Decimal
from enum import Enum


class OperationType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class WalletOperation(BaseModel):
    operation_type: OperationType
    amount: Decimal = Field(ge=0.01, decimal_places=2)


class WalletResponse(BaseModel):
    balance: Decimal = Field(decimal_places=2)
