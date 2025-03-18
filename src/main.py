from fastapi import FastAPI
from api.v1.wallets import main_router


app = FastAPI(title="Wallet API",
              description="API для управления кошельками",
              version="1.0.0")
app.include_router(main_router)
