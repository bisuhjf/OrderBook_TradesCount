import http.client
import pandas as pd
import json, hmac, hashlib, time, requests


cb_symbol = 'BTC-USD'


def cb_ob(symbol):
    conn = http.client.HTTPSConnection("api.exchange.coinbase.com")
    payload = ''
    headers = {'Content-Type': 'application/json'}
    url = "/products/{}/book?level=2".format(symbol)
    conn.request("GET", url, payload, headers=headers)
    res = conn.getresponse()
    if res.status == 200:
        data = res.read().decode("utf-8")
        order_book = json.loads(data)
        bids = order_book['bids']
        asks = order_book['asks']
        bids_df = pd.DataFrame(bids, columns=['price', 'volume', 'num'])[0:10].astype(float)
        asks_df = pd.DataFrame(asks, columns=['price', 'volume', 'num'])[0:10].astype(float)
        mid = (bids_df['price'].iloc[0] + asks_df['price'].iloc[0]) / 2
        bids_df['diff'] = mid - bids_df['price']
        asks_df['diff'] = asks_df['price'] - mid
        bids_df['diff_volume'] = bids_df['diff'] * bids_df['volume']
        asks_df['diff_volume'] = asks_df['diff'] * asks_df['volume']
        bids_sum = sum(bids_df['diff_volume'])
        asks_sum = sum(asks_df['diff_volume'])
    else:
        print('Coinbase Error Code: {}'.format(res.status))
        bids_sum, asks_sum, mid = 0, 0, 0
    return bids_sum, asks_sum, mid


