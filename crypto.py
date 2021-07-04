import requests 
import os

from requests.exceptions import ConnectionError, Timeout, TooManyRedirects


CRYPTO_KEY = os.getenv("CRYPTO_KEY")
CRYPTO_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
MAX_API_REQUESTS = 5
superfluous_parameters = (
        'slug', 'date_added', 'tags', 'num_market_pairs', 'platform', 
        'last_updated'
    )   


class CoinMarketCrypto:
    def __init__(self, min=1, max=500, fiat_currency='USD', url=CRYPTO_URL):
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': CRYPTO_KEY,
            "Accept-Encoding": "deflate, gzip"
        }

        self.parameters = {
            'start': min,
            'limit': max,
            'convert': fiat_currency
        }

        self.run(url=url, fiat_currency=fiat_currency)

    def run(self, url, fiat_currency):
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.load_data(url)
        self.catch_error()
        self.clean_data()
        self.return_detailed_prices(fiat_currency)

    
    def load_data(self, url):
        try:
            get = self.session.get(url, params=self.parameters)
            self.file = get.json()
        except(ConnectionError, Timeout, TooManyRedirects) as e:
            print("Something went wrong and the API said: '%s'" %e)

    def catch_error(self):
        try:
            self.status = self.file['status']['error_code'] 
            if self.status != 200 and self.status != 0:
                error_message = self.file['status']['error_message']
                raise Exception("Something went wrong with making that request: "
                                "%s" %(error_message))
        except:
            self.status, error_message = self.file['statusCode'], self.file['error']
            raise Exception("Something went wrong with making that request: "
                            "%s" %(error_message))
    
    def delete(self, crypto, args):
        try:
            for arg in args:
                del crypto[arg]          
        except KeyError as e:
            new_args = tuple(x for x in args if x != e)
            self.delete(crypto, new_args)
            print("You inputted an invalid key '%s' into your dictionary" %(e))

    def clean_data(self):
        self.data = self.file['data']
        for crypto in self.data:
            self.delete(crypto, superfluous_parameters)
    
    def calculate_time_parameters(self):
        self.timestamp = self.file['status']['timestamp']

        timestamp_values = self.timestamp.replace("T", '-').split("-")
        self.year, self.month, self.day, self.time = tuple(timestamp_values)

        time_values = self.time.replace(".", ':').split(":")
        self.hour, self.minute, self.second, self.millisecond = tuple(time_values)


    def return_detailed_prices(self, fiat_currency):
        self.quote = {}
        for crypto in self.data:
            prices = {}
            name, symbol = crypto['name'].lower(), crypto['symbol'].lower()
            quotes = crypto['quote'][fiat_currency]
            
            prices['24 Hour Volume'] = quotes['volume_24h']
            prices['Percent Change Within Past Hour'] = quotes['percent_change_1h']
            prices['Percent Change Within Past 24 Hours'] = quotes['percent_change_24h']
            prices['Percent Change Within Past 7 Days'] = quotes['percent_change_7d']
            prices['Percent Change Within Past 30 Days'] = quotes['percent_change_30d']
            prices['Percent Change Within Past 60 Days'] = quotes['percent_change_60d']
            prices['Percent Change Within Past 90 Days'] = quotes['percent_change_90d']

            # user should input symbol or name into bot and get the same values
            self.quote[name] = prices
            self.quote[symbol] = prices



