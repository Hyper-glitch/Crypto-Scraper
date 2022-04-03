import csv
import os
import urllib.parse as urllib

import requests


class CoinApi:
    def __init__(self, api_key):
        self.base_url = 'https://rest.coinapi.io/v1/'
        self.auth = {'X-CoinAPI-Key': f'{api_key}'}
        self.session = requests.Session()
        self.session.headers.update(self.auth)

    def get_exchanges(self, filter_exchange_ids):
        endpoint = 'exchanges'
        url = urllib.urljoin(self.base_url, endpoint)
        params = {'filter_exchange_id': filter_exchange_ids,
                  }
        response = self.session.get(url=url, params=params)
        response.raise_for_status()
        return response.json()

    def get_historical_data(self, coin_name, asset_id_quote, period_id, time_start, time_end, limit):
        endpoint = f'exchangerate/{coin_name}/{asset_id_quote}/history'
        url = urllib.urljoin(self.base_url, endpoint)
        params = {'period_id': period_id,
                  'time_start': time_start,
                  'time_end': time_end,
                  'limit': limit,
                  }
        response = self.session.get(url=url, params=params)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def save_to_csv(currencies, csv_name):
        field_names = currencies[0].keys()
        with open(f'currencies_data/{csv_name}.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(currencies)


def prepare_exchanges_data(currencies):
    for currency in currencies:
        currency_name = currency['exchange_id']
        pass


if __name__ == '__main__':
    API_KEY = os.environ.get('COIN_API_KEY')

    coin_instance = CoinApi(api_key=API_KEY)

    filter_exchange_ids = 'BITSTAMP;GEMINI'
    output_format = 'csv'
    coin_name = 'BTC'
    asset_id_quote = 'USD'
    period_id = '5MIN'
    time_start = '2022-03-01T00:00:00'
    time_end = '2022-03-05T00:00:00'
    limit = 10000

    # currencies = coin_instance.get_exchanges(filter_exchange_ids, output_format)

    historical_data = coin_instance.get_historical_data(
        coin_name=coin_name, asset_id_quote=asset_id_quote, period_id=period_id,
        time_start=time_start, time_end=time_end, limit=limit,
    )

    csv_name = 'historical_data'
    coin_instance.save_to_csv(currencies=historical_data, csv_name=csv_name)
