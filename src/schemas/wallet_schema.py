from pydantic import BaseModel, Field
from decimal import Decimal
from enum import Enum
from uuid import UUID


class OperationType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class WalletOperation(BaseModel):
    operation_type: OperationType
    amount: Decimal = Field(ge=0.01, decimal_places=2)


class WalletResponse(BaseModel):
    wallet_id: UUID = Field()
    balance: float = Field()
