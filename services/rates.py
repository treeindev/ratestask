from database import Database
from datetime import datetime, timedelta
from services.exchange_rates import ExchangeRatesService

class RatesService:
    def __init__(self):
        self.database = Database()
        self.exchangeService = ExchangeRatesService()
        
    def get_rate(self, allow_null, date_from, date_to, origin, destination):
        self.database.connect()
        cursor = self.database.query(
            """
                SELECT day, ROUND(AVG(price),2) AS price, COUNT(price) AS times
                FROM prices 
                WHERE 
                    (day BETWEEN %s::date AND %s::date) AND
                    (orig_code IN (SELECT code FROM ports WHERE code=%s OR parent_slug=%s)) AND
                    (dest_code IN (SELECT code FROM ports WHERE code=%s OR parent_slug=%s))
                GROUP BY day
                ORDER BY day ASC;
            """,
            (date_from, date_to, origin, origin, destination, destination)
        )
        rates = cursor.fetchall()
        self.database.close()

        if not allow_null:
            return [{"day":f"{rate[0]}","average_price":float(rate[1])} for rate in rates]

        collection = []
        for rate in rates:
            if rate[2]<3:
                collection.append({"day":f"{rate[0]}","average_price":None})
            else:
                collection.append({"day":f"{rate[0]}","average_price":float(rate[1])})
        return collection

    def create_rate(self, date_from, date_to, origin_code, destination_code, price, currency):
        price = self.exchangeService.get_default_price(price, currency)
        fr = datetime.strptime(date_from, "%Y-%m-%d")
        to = datetime.strptime(date_to, "%Y-%m-%d")
        days = (to-fr).days
        
        self.database.connect()
        for x in range(days):
            date = fr + timedelta(days=x)
            cursor = self.database.query(
                """   
                    INSERT INTO prices (orig_code, dest_code, day, price)
                    VALUES(%s, %s, %s, %s)
                """,
                (origin_code, destination_code, date, price)
            )
        self.database.close()
        