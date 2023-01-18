from fastapi import APIRouter, Depends
from fastapi.security.api_key import APIKey

from app.auth import get_api_key
from app.modules.currencies.defaults import CurrencyCodeEnum

from .schemas import Conversion
from .services import CurrencyService

currency_router = APIRouter()


@currency_router.get("/convert", response_model=Conversion)
async def convert(
    ammount: float,
    from_currency: CurrencyCodeEnum,
    to_currency: CurrencyCodeEnum,
    api_key: APIKey = Depends(get_api_key),
):
    """Converts ammount from one currency to another. Calculates the mid-market rate.

    Args:
        ammount (float): The ammount to be converted
        from_currency (CurrencyCodeEnum): The currency to be converted from
        to_currency (CurrencyCodeEnum): The currency to be converted to

    Returns:
        Conversion: A dictionary containing the converted ammount, the mid-market rate
        and metadata about the conversion.
    """
    currency_service = CurrencyService()
    conversion = currency_service.convert(
        ammount=ammount, from_currency=from_currency.value, to_currency=to_currency.value
    )
    currency_service.save_conversion(conversion)
    return conversion


@currency_router.get("/currencies", response_model=dict[str, str])
async def get_currencies(api_key: APIKey = Depends(get_api_key)):
    """Gets a dictionary with all available currencies in the format:
    { currency_name: currency_code }.

    Args:
        api_key (APIKey, optional): The API Key. Defaults to Depends(get_api_key).

    Returns:
        Dict[str, str]: A dictionary with all available currencies.
    """
    currency_service = CurrencyService()
    currencies = currency_service.get_currencies_from_wise_api()
    return currencies


@currency_router.get("/history", response_model=list[Conversion])
async def get_history(api_key: APIKey = Depends(get_api_key)):
    """Gets all previous conversions.

    Args:
        api_key (APIKey, optional): The API Key. Defaults to Depends(get_api_key).

    Returns:
        list[Conversion]: A list with all previously made conversions.
    """
    currency_service = CurrencyService()
    currencies = currency_service.get_history()
    return currencies
