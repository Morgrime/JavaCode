from wallet_router import router as wallet_router
from fastapi import APIRouter


main_router = APIRouter()
main_router.include_router(wallet_router)
