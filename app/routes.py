from fastapi import FastAPI

from app.modules.currencies.routes import currency_router


def init_app(app: FastAPI):
    app.include_router(currency_router, tags=["Currencies"])
