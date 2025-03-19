from uuid import UUID
from decimal import Decimal
from sqlalchemy import select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.wallet_model import Wallet


# добавление кошелька
async def add_wallet(session: AsyncSession) -> UUID:
    result = await session.execute(
        insert(Wallet).values(balance=0.00))
    await session.commit()
    return result.inserted_primary_key[0]


# удаление кошелька
async def delete_wallet(session: AsyncSession, wallet_uuid: UUID) -> bool:
    result = await session.execute(
        delete(Wallet).where(Wallet.id == wallet_uuid))
    await session.commit()
    return result.rowcount > 0


# получение баланса
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
    db: AsyncSession,
    wallet_uuid: UUID,
    operation_type: str,
    amount: Decimal
) -> Decimal:
    """
    Выполняет операцию с кошельком (пополнение или списание).
    - **wallet_uuid**: UUID кошелька.
    - **operation_type**: DEPOSIT (пополнение) или WITHDRAW (списание).
    - **amount**: Сумма операции.
    - **return**: Новый баланс кошелька.
    """
    async with db.begin():  # Начинаем транзакцию
        # Получаем текущий баланс с блокировкой строки
        result = await db.execute(
            select(Wallet.balance)
            .where(Wallet.id == wallet_uuid)
            .with_for_update()
        )
        wallet = result.scalar_one_or_none()

        if wallet is None:
            raise ValueError(f"Wallet with UUID {wallet_uuid} not found")

        # Выполняем операцию
        if operation_type == "DEPOSIT":
            new_balance = wallet + amount
        elif operation_type == "WITHDRAW":
            if wallet < amount:
                raise ValueError("Insufficient funds")
            new_balance = wallet - amount
        else:
            raise ValueError("Invalid operation type")

        # Обновляем баланс
        await db.execute(
            update(Wallet)
            .where(Wallet.id == wallet_uuid)
            .values(balance=new_balance)
        )

        return new_balance
