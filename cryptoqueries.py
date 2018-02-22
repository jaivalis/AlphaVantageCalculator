import logging
import os

import pandas as pd
from alpha_vantage.cryptocurrencies import CryptoCurrencies

API_KEY = os.environ['API_KEY']

cc = None
df = None

CLOSE_COLUMN_NAME = '4a. close (USD)'
CLOSE_COLUMN_NAME_CLEAN = 'close'


def fetch_daily_btc_closing_prices():
    global cc
    global df
    
    if df is None:
        logging.info("Asking AV for data.")
        cc = CryptoCurrencies(key=API_KEY, output_format='pandas')
        df, meta_data = cc.get_digital_currency_daily(symbol='BTC', market='USD')
        df = df.filter([CLOSE_COLUMN_NAME])
        df = df.rename(columns={CLOSE_COLUMN_NAME: CLOSE_COLUMN_NAME_CLEAN})
        df.index = pd.to_datetime(df.index, format='%Y-%m-%d')
        logging.info("Done.")
    return df
