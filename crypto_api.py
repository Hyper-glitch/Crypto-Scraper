import csv
import os
import urllib.parse as urllib

import requests


class NomicsApi:
    def __init__(self, api_key):
        self.base_url = 'https://api.nomics.com/v1/'
        self.api_key = api_key
        self.session = requests.Session()

    def get_currencies(self):
        endpoint = 'currencies/ticker'
        url = urllib.urljoin(self.base_url, endpoint)
        params = {'key': f'{self.api_key}',
                  'ids': 'BTC',
                  'interval': '1d, 7d',
                  'per-page': 100,
                  'page': 1,
                  }
        response = self.session.get(url=url, params=params)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def save_to_csv(currencies):
        field_names = currencies[0].keys()
        with open('currencies.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(currencies)


if __name__ == '__main__':
    API_KEY = os.environ.get('API_KEY')

    nomics_instance = NomicsApi(api_key=API_KEY)
    currencies = nomics_instance.get_currencies()
    nomics_instance.save_to_csv(currencies=currencies)
