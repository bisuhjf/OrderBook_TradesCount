import pandas as pd
import requests


bn_host = 'https://api.binance.com'
bn_prefix = '/api/v3/depth'
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
symbol_usdt = 'BTCUSDT'
symbol_fdusd = 'BTCFDUSD'
limit = 10


def bn_ob(symbol):
    bn_url = '{}{}?symbol={}&limit={}'.format(bn_host, bn_prefix, symbol, limit)
    response = requests.request('GET', bn_url, headers=headers)
    if response.status_code == 200:
        depth_info = response.json()
        bids_df = pd.DataFrame(depth_info['bids'], columns=['price', 'volume']).astype(float)
        asks_df = pd.DataFrame(depth_info['asks'], columns=['price', 'volume']).astype(float)
        mid = (bids_df['price'].iloc[0] + asks_df['price'].iloc[0]) / 2
        bids_df['diff'] = mid - bids_df['price']
        asks_df['diff'] = asks_df['price'] - mid
        bids_df['diff_volume'] = bids_df['diff'] * bids_df['volume']
        asks_df['diff_volume'] = asks_df['diff'] * asks_df['volume']
        bids_sum = sum(bids_df['diff_volume'])
        asks_sum = sum(asks_df['diff_volume'])
    else:
        print('Error: {}, {}'.format(response.status_code, response.json()))
        bids_sum, asks_sum = 0, 0
    return bids_sum, asks_sum
