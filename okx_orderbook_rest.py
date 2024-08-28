import base64
import hmac
import json
import time
import requests
import numpy as np
import pandas as pd


ok_symbol = 'BTC-USDT'


def ok_ob(symbol):
    url = "https://www.okx.com/api/v5/market/books"
    params = {'instId': symbol, 'sz': 10}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        ob = response.json()
        data = ob['data']
        asks = data[0]['asks']
        bids = data[0]['bids']
        asks_df = pd.DataFrame(asks, columns=['price', 'volume', 'num1', 'num2'])[0:10].astype(float)
        bids_df = pd.DataFrame(bids, columns=['price', 'volume', 'num1', 'num2'])[0:10].astype(float)
        mid = (asks_df['price'].iloc[0] + bids_df['price'].iloc[0]) / 2
        bids_df['diff'] = mid - bids_df['price']
        asks_df['diff'] = asks_df['price'] - mid
        bids_df['diff_volume'] = bids_df['diff'] * bids_df['volume']
        asks_df['diff_volume'] = asks_df['diff'] * asks_df['volume']
        bids_sum = sum(bids_df['diff_volume'])
        asks_sum = sum(asks_df['diff_volume'])
    else:
        print('Error Code: {}'.format(response.status_code))
        bids_sum, asks_sum, mid = 0, 0, 0
    return bids_sum, asks_sum, mid

