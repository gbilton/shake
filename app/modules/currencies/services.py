from datetime import datetime
from typing import Any

import requests
from bs4 import BeautifulSoup

from app.db import get_database
from app.modules.currencies.defaults import wise_authorization
from app.modules.currencies.schemas import Conversion, ConversionMetadata


class CurrencyService:
    def __init__(self):
        self.db = get_database()

    def convert(self, ammount: float, from_currency: str, to_currency: str) -> Conversion:
        """Converts ammount from one currency to another.

        Args:
            ammount (float): The Ammount to be converted
            from_currency (str): The currency to convert from
            to_currency (str): The currency to convert to

        Returns:
            Conversion: A conversion object with data about the conversion.
        """
        raw_response = self._get_conversion_from_wise_api(
            from_currency=from_currency, to_currency=to_currency
        )

        rate = raw_response["rate"]
        converted_ammount = self._calculate_converted_ammount(ammount, rate)
        conversion_response = Conversion(
            converted_amount=converted_ammount,
            rate=rate,
            metadata=ConversionMetadata(
                time_of_conversion=datetime.strptime(raw_response["time"], "%Y-%m-%dT%H:%M:%S%z"),
                from_currency=from_currency,
                to_currency=to_currency,
            ),
        )
        return conversion_response

    def _calculate_converted_ammount(self, ammount: float, rate: float) -> float:
        """Calculates the converted ammount

        Args:
            ammount (float): The ammount to be converted
            rate (float): The conversion rate

        Returns:
            float: The converted ammount.
        """
        return ammount * rate

    def _get_conversion_from_wise_api(self, from_currency: str, to_currency: str) -> dict[str, Any]:
        """Gets the conversion from the wise API.

        Args:
            from_currency (str): The currency to convert from
            to_currency (str): The currency to convert to

        Raises:
            Exception: _description_

        Returns:
            dict[str, Any]: The json data from the response.
        """
        wise_api_url = f"https://api.wise.com/v1/rates?source={from_currency}&target={to_currency}"
        headers = {"authorization": wise_authorization}

        r = requests.get(wise_api_url, headers=headers)

        if r.status_code != 200:
            raise Exception

        return r.json()[0]

    def get_currencies_from_wise_api(self) -> dict[str, str]:
        """Gets all currencies available in the wise API

        Raises:
            Exception: _description_

        Returns:
            dict[str, str]: A dictionary containing all available currencies and their codes.
        """
        wise_currencies_url = "https://wise.com/gb/currency-converter/currencies"
        r = requests.get(wise_currencies_url)

        if r.status_code != 200:
            raise Exception

        currencies_dict = self._parse_currencies(r.text)

        return currencies_dict

    def _parse_currencies(self, html_text: str) -> dict[str, str]:
        """Creates a dictionary from the wise currency page's html,
        in the format { currency_name: currency:code }

        Args:
            html_text (str): The HTML from the wise currency page.

        Returns:
            dict[str, str]: A dictionary with the name and code of the available currencies.
        """
        soup = BeautifulSoup(html_text, "html.parser")
        currency_name_class = "currencies_currencyCard__currencyName__wj5_u"
        currency_code_class = "currencies_currencyCard__currencyCode__RG8bp"
        currency_names = soup.find_all(class_=currency_name_class)
        currency_codes = soup.find_all(class_=currency_code_class)

        return {
            currency_name.text: currency_code.text
            for currency_name, currency_code in zip(currency_names, currency_codes)
        }

    def get_history(self) -> list[Conversion]:
        """Gets all past conversions from the database.

        Returns:
            list[Conversion]: A list with information about all past conversions.
        """
        conversions_cursor = self.db["conversions"].find({})
        past_conversions = [Conversion(**conversion) for conversion in conversions_cursor]
        return past_conversions

    def save_conversion(self, conversion: Conversion):
        """Saves a conversion to the database."""
        conversion_dict = conversion.dict()
        self.db["conversions"].insert_one(conversion_dict)
