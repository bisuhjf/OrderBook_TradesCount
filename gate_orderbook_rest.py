import pandas as pd
import requests


gate_symbol = 'BTC_USDT'
host = "https://api.gateio.ws"
prefix = "/api/v4"
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
limit = 10


def get_order_book(symbol):
    url = '/spot/order_book'
    query_param = 'currency_pair={}&limit={}'.format(symbol, limit)
    response = requests.request('GET', host + prefix + url + "?" + query_param, headers=headers)
    if response.status_code == 200:
        order_book = response.json()
        bids = order_book['bids']
        asks = order_book['asks']
        bids_df = pd.DataFrame(bids, columns=['price', 'volume']).astype(float)
        asks_df = pd.DataFrame(asks, columns=['price', 'volume']).astype(float)
        mid = (bids_df['price'].iloc[0] + asks_df['price'].iloc[0]) / 2
        bids_df['diff'] = mid - bids_df['price']
        asks_df['diff'] = asks_df['price'] - mid
        bids_df['diff_volume'] = bids_df['diff'] * bids_df['volume']
        asks_df['diff_volume'] = asks_df['diff'] * asks_df['volume']
        bids_sum = sum(bids_df['diff_volume'])
        asks_sum = sum(asks_df['diff_volume'])
    else:
        print('Binance Error Code: {}'.format(response.status_code))
        bids_sum, asks_sum, mid = 0, 0, 0
    return bids_sum, asks_sum, mid


# print(get_order_book(gate_symbol))

