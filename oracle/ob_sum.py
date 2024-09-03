from binance_orderbook_rest import bn_ob
from coinbase_orderbook_rest import cb_ob
from okx_orderbook_rest import ok_ob
from bybit_orderbook_rest import bb_ob
from gate_orderbook_rest import gt_ob
from kraken_orderbook_rest import kk_ob
import pandas as pd
import time


ob_df = pd.DataFrame({'bn_usdt_bids': [0], 'bn_usdt_asks': [0],
                      'bn_fdusd_bids': [0], 'bn_fdusd_asks': [0],
                      'cb_bids': [0], 'cb_asks': [0],
                      'ok_bids': [0], 'ok_asks': [0],
                      'bb_bids': [0], 'bb_asks': [0],
                      'gt_bids': [0], 'gt_asks': [0],
                      'kk_bids': [0], 'kk_asks': [0],
                      },
                     columns=['bn_usdt_bids', 'bn_usdt_asks',
                              'bn_fdusd_bids', 'bn_fdusd_asks',
                              'cb_bids', 'cb_asks',
                              'ok_bids', 'ok_asks',
                              'bb_bids', 'bb_asks',
                              'gt_bids', 'gt_asks',
                              'kk_bids', 'kk_asks',
                              ]
                     )


def ob_sum():
    global ob_df
    while True:
        bn_usdt_bids, bn_usdt_asks, bn_usdt_mid = bn_ob(symbol='BTCUSDT')
        bn_fdusd_bids, bn_fdusd_asks, bn_fdusd_mid = bn_ob(symbol='BTCFDUSD')
        cb_bids, cb_asks, cb_mid = cb_ob(symbol='BTC-USD')
        ok_bids, ok_asks, ok_mid = ok_ob(symbol='BTC-USDT')
        bb_bids, bb_asks, bb_mid = bb_ob(symbol='BTCUSDT')
        gt_bids, gt_asks, gt_mid = gt_ob(symbol='BTC_USDT')
        kk_bids, kk_asks, kk_mid = kk_ob(symbol='BTC/USD')

        mid_price = (bn_usdt_mid + bn_fdusd_mid + cb_mid + ok_mid + bb_mid) / 5

        new_row = pd.DataFrame({'bn_usdt_bids': [bn_usdt_bids], 'bn_usdt_asks': [bn_usdt_asks],
                                'bn_fdusd_bids': [bn_fdusd_bids], 'bn_fdusd_asks': [bn_fdusd_asks],
                                'cb_bids': [cb_bids], 'cb_asks': [cb_asks],
                                'ok_bids': [ok_bids], 'ok_asks': [ok_asks],
                                'bb_bids': [bb_bids], 'bb_asks': [bb_asks],
                                'gt_bids': [gt_bids], 'gt_asks': [gt_asks],
                                'kk_bids': [kk_bids], 'kk_asks': [kk_asks],
                                'mid_price': [mid_price],
                                },
                               columns=['bn_usdt_bids', 'bn_usdt_asks',
                                        'bn_fdusd_bids', 'bn_fdusd_asks',
                                        'cb_bids', 'cb_asks',
                                        'ok_bids', 'ok_asks',
                                        'bb_bids', 'bb_asks',
                                        'gt_bids', 'gt_asks',
                                        'kk_bids', 'kk_asks',
                                        'mid_price',
                                        ]
                               )
        ob_df = pd.concat([ob_df, new_row], ignore_index=True)
        time.sleep(0.5)
        if len(ob_df) > 120:
            ob_df = ob_df.drop(0)
            # bid_sum_list = (
            #         ob_df['bn_usdt_bids']
            #         + ob_df['bn_fdusd_bids']
            #         + ob_df['cb_bids']
            #         + ob_df['ok_bids']
            #         + ob_df['bb_bids']
            # )
            # ask_sum_list = (
            #         ob_df['bn_usdt_asks']
            #         + ob_df['bn_fdusd_asks']
            #         + ob_df['cb_asks']
            #         + ob_df['ok_asks']
            #         + ob_df['bb_asks']
            # )

            # bid_ask = bid_sum_list - ask_sum_list
            # bid_ask_mean = bid_ask.mean()
            # bid_ask_std = bid_ask.std()
            # top = bid_ask_mean + 2 * bid_ask_std
            # bottom = bid_ask_mean - 2 * bid_ask_std
            # top_bid_ask = top - bid_ask.iloc[-1]
            # bid_ask_bottom = bid_ask.iloc[-1] - bottom
            #
            # mid_price_list = ob_df['mid_price']
            # mid_price_diff = mid_price_list.iloc[-1] - mid_price_list.iloc[0]

            return ob_df



