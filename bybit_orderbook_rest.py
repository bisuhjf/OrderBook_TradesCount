import requests
import pandas as pd


bb_symbol = 'BTCUSDT'


def bb_ob(symbol):
    url = "https://api.bybit.com/v5/market/orderbook"
    params = {'category': 'spot', 'symbol': symbol, 'limit': 10}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        ob = response.json()
        data = ob['result']
        bids = data['b']
        asks = data['a']
        asks_df = pd.DataFrame(asks, columns=['price', 'volume'])[0:10].astype(float)
        bids_df = pd.DataFrame(bids, columns=['price', 'volume'])[0:10].astype(float)
        mid = (asks_df['price'].iloc[0] + bids_df['price'].iloc[0]) / 2
        bids_df['diff'] = mid - bids_df['price']
        asks_df['diff'] = asks_df['price'] - mid
        bids_df['diff_volume'] = bids_df['diff'] * bids_df['volume']
        asks_df['diff_volume'] = asks_df['diff'] * asks_df['volume']
        bids_sum = sum(bids_df['diff_volume'])
        asks_sum = sum(asks_df['diff_volume'])
    else:
        print("Error Code: {}".format(response.status_code))
        bids_sum, asks_sum = 0, 0
    return bids_sum, asks_sum



