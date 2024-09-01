import requests
import pandas as pd


kraken_symbol = 'BTC/USD'
limit = 10


def get_order_book(symbol):
    url = "https://api.kraken.com/0/public/Depth?pair={}&count={}".format(symbol, limit)
    params = {'pair': 'XBTUSD', 'count': 10}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        order_book = response.json()
        bids = order_book['result'][symbol]['bids']
        asks = order_book['result'][symbol]['asks']
        bids_df = pd.DataFrame(bids, columns=['price', 'volume', 'timestamp']).astype(float)
        asks_df = pd.DataFrame(asks, columns=['price', 'volume', 'timestamp']).astype(float)
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
