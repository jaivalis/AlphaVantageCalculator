from alpha_vantage.cryptocurrencies import CryptoCurrencies

import os


API_KEY = os.environ['API_KEY']

cc = None

df = None


def fetch_daily_btc_closing_prices():
    global cc
    global df
    
    if df is None:
        print("Asking AV for data.")
        cc = CryptoCurrencies(key=API_KEY, output_format='pandas')
        df, meta_data = cc.get_digital_currency_daily(symbol='BTC', market='USD')
        df = df.filter(['4a. close (USD)'])
        df = df.rename(columns={'4a. close (USD)': 'close'})
        print("[DONE]")
    
    return df
