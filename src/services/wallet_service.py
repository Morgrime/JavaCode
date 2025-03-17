from uuid import UUID
from decimal import Decimal
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.wallet_model import Wallet


async def get_wallet_balance(
    session: AsyncSession,
    wallet_uuid: UUID
) -> Decimal | None:
    result = await session.execute(
        select(Wallet.balance)
        .where(Wallet.id == wallet_uuid)
        .with_for_update()  # Блокировка для конкурентных запросов
    )
    return result.scalar_one_or_none()


async def process_wallet_operation(
    session: AsyncSession,
    wallet_uuid: UUID,
    operation_type: str,
    amount: Decimal
) -> Decimal:
    # Начинаем транзакцию
    async with session.begin():
        wallet = await session.get(Wallet, wallet_uuid, with_for_update=True)

        if not wallet:
            raise ValueError("Wallet not found")

        if operation_type == "DEPOSIT":
            new_balance = wallet.balance + amount
        elif operation_type == "WITHDRAW":
            if wallet.balance < amount:
                raise ValueError("Insufficient funds")
            new_balance = wallet.balance - amount
        else:
            raise ValueError("Invalid operation type")

        # Обновляем баланс через SQL выражение для атомарности
        await session.execute(
            update(Wallet)
            .where(Wallet.id == wallet_uuid)
            .values(balance=new_balance)
        )

        return new_balance
