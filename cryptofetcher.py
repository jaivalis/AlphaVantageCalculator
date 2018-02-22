import logging
import os

import pandas as pd
from alpha_vantage.cryptocurrencies import CryptoCurrencies

API_KEY = os.environ['API_KEY']

CLOSE_COLUMN_NAME = '4a. close (USD)'
CLOSE_COLUMN_NAME_CLEAN = 'close'


class CryptoFetcher(object):
    def __init__(self):
        logging.info("Asking AV for data.")
        cc = CryptoCurrencies(key=API_KEY, output_format='pandas')
        self.df, meta_data = cc.get_digital_currency_daily(symbol='BTC', market='USD')
        self.df = self.df.filter([CLOSE_COLUMN_NAME])
        self.df = self.df.rename(columns={CLOSE_COLUMN_NAME: CLOSE_COLUMN_NAME_CLEAN})
        self.df.index = pd.to_datetime(self.df.index, format='%Y-%m-%d')
        logging.info("Done.")
