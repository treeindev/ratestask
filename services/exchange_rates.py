import ast
import os
import requests
import constants

class ExchangeRatesService:
    def __init__(self):
        self.rates_domain = "https://openexchangerates.org/api/"

    def get_default_price(self, price, currency):
        if currency == constants.DEFAULT_CURRENCY:
            return price
            
        rates_id = os.getenv("ID_EXCHANGE_RATE")
        req_rates = requests.get( f"{self.rates_domain}latest.json?app_id={rates_id}")
        rate = ast.literal_eval(req_rates.text)['rates'][currency]
        return price / rate
