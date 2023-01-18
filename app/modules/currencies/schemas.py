from datetime import datetime

from pydantic import BaseModel

from app.modules.currencies.defaults import CurrencyCodeEnum


class ConversionMetadata(BaseModel):
    time_of_conversion: datetime
    from_currency: str
    to_currency: str


class Conversion(BaseModel):
    converted_amount: float
    rate: float
    metadata: ConversionMetadata


class Currency(BaseModel):
    currency: CurrencyCodeEnum
