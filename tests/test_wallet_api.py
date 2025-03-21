import pytest
from fastapi import status
from uuid import UUID

# Создание кошелька
@pytest.mark.asyncio
async def test_create_wallet(client):
    response = await client.post("/api/v1/wallets")
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "wallet_id" in data
    assert "balance" in data
    assert data["balance"] == 0.00

# Пополнение кошелька
@pytest.mark.asyncio
async def test_deposit_operation(client):
    # Создание кошелька
    create_response = await client.post("/api/v1/wallets")
    wallet_id = create_response.json()["wallet_id"]

    # Пополнение
    deposit_response = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "DEPOSIT", "amount": 1000}
    )
    assert deposit_response.status_code == status.HTTP_200_OK
    data = deposit_response.json()
    assert data["balance"] == 1000.00

# Вывод средств
@pytest.mark.asyncio
async def test_withdraw_operation(client):
    # Создание кошелька
    create_response = await client.post("/api/v1/wallets")
    wallet_id = create_response.json()["wallet_id"]

    # Пополнение
    await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "DEPOSIT", "amount": 1000}
    )

    # Вывод средств
    withdraw_response = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "WITHDRAW", "amount": 500}
    )
    assert withdraw_response.status_code == status.HTTP_200_OK
    data = withdraw_response.json()
    assert data["balance"] == 500.00

# Получение баланса
@pytest.mark.asyncio
async def test_get_balance(client):
    # Создание кошелька
    create_response = await client.post("/api/v1/wallets")
    wallet_id = create_response.json()["wallet_id"]

    # Получение баланса
    balance_response = await client.get(f"/api/v1/wallets/{wallet_id}")
    assert balance_response.status_code == status.HTTP_200_OK
    data = balance_response.json()
    assert data["balance"] == 0.00

# Удаление кошелька
@pytest.mark.asyncio
async def test_delete_wallet(client):
    # Создание кошелька
    create_response = await client.post("/api/v1/wallets")
    wallet_id = create_response.json()["wallet_id"]

    # Удаление кошелька
    delete_response = await client.delete(f"/api/v1/wallets/{wallet_id}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    # Проверка, что кошелек удален
    balance_response = await client.get(f"/api/v1/wallets/{wallet_id}")
    assert balance_response.status_code == status.HTTP_404_NOT_FOUND