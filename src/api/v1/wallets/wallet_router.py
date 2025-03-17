from fastapi import APIRouter, HTTPException
from uuid import UUID

router = APIRouter(prefix="/api/v1/wallets")


@router.get("/{WALLET_UUID}")
async def get_wallet_action(wallet_uuid: UUID,):
    pass


@router.post("api/v1/wallets/{WALLET_UUID}/{operation}")
async def update_wallet_action(wallet_uuid: UUID,):
    pass