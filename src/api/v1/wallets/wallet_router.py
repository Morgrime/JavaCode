from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from schemas.wallet_schema import WalletOperation, WalletResponse
from services.wallet_service import (
    get_wallet_balance,
    process_wallet_operation
)
from database.session import get_session  # Обновленный импорт

router = APIRouter(prefix="/api/v1/wallets", tags=["Wallets"])


@router.get("/{wallet_uuid}", response_model=WalletResponse)
async def get_balance(
    wallet_uuid: UUID,
    db: Annotated[AsyncSession, Depends(get_session)]  # Используем get_session
) -> WalletResponse:
    """
    Получение текущего баланса кошелька
    - **wallet_uuid**: UUID кошелька (формат UUIDv4)
    - **return**: Текущий баланс и статус кошелька
    """
    balance = await get_wallet_balance(db, wallet_uuid)
    if balance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )
    return WalletResponse(balance=balance)


@router.post("/{wallet_uuid}/operation", status_code=status.HTTP_200_OK)
async def perform_operation(
    wallet_uuid: UUID,
    operation: WalletOperation,
    db: Annotated[AsyncSession, Depends(get_session)]  # Используем get_session
) -> WalletResponse:
    """
    Выполнение операции с кошельком
    - **wallet_uuid**: UUID кошелька
    - **operation_type**: DEPOSIT (пополнение) или WITHDRAW (списание)
    - **amount**: Сумма операции (положительное число)
    - **return**: Обновленный баланс после операции
    """
    try:
        new_balance = await process_wallet_operation(
            db=db,
            wallet_uuid=wallet_uuid,
            operation_type=operation.operation_type,
            amount=operation.amount
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    return WalletResponse(balance=new_balance)
