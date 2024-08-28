from binance_orderbook_rest import bn_ob
from coinbase_orderbook_rest import cb_ob
from okx_orderbook_rest import ok_ob
from bybit_orderbook_rest import bb_ob
import pandas as pd
import time


ob_df = pd.DataFrame({'bn_usdt_bids': [0], 'bn_usdt_asks': [0],
                      'bn_fdusd_bids': [0], 'bn_fdusd_asks': [0],
                      'cb_bids': [0], 'cb_asks': [0],
                      'ok_bids': [0], 'ok_asks': [0],
                      'gt_bids': [0], 'gt_asks': [0],
                      'bb_bids': [0], 'bb_asks': [0],
                      },
                     columns=['bn_usdt_bids', 'bn_usdt_asks',
                              'bn_fdusd_bids', 'bn_fdusd_asks',
                              'cb_bids', 'cb_asks',
                              'ok_bids', 'ok_asks',
                              'gt_bids', 'gt_asks',
                              'bb_bids', 'bb_asks',
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

        mid_price = (bn_usdt_mid + bn_fdusd_mid + cb_mid + ok_mid + bb_mid) / 5

        new_row = pd.DataFrame({'bn_usdt_bids': [bn_usdt_bids], 'bn_usdt_asks': [bn_usdt_asks],
                                'bn_fdusd_bids': [bn_fdusd_bids], 'bn_fdusd_asks': [bn_fdusd_asks],
                                'cb_bids': [cb_bids], 'cb_asks': [cb_asks],
                                'ok_bids': [ok_bids], 'ok_asks': [ok_asks],
                                'bb_bids': [bb_bids], 'bb_asks': [bb_asks],
                                'mid_price': [mid_price],
                                },
                               columns=['bn_usdt_bids', 'bn_usdt_asks',
                                        'bn_fdusd_bids', 'bn_fdusd_asks',
                                        'cb_bids', 'cb_asks',
                                        'ok_bids', 'ok_asks',
                                        'bb_bids', 'bb_asks',
                                        'mid_price',
                                        ]
                               )
        ob_df = pd.concat([ob_df, new_row], ignore_index=True)
        time.sleep(0.5)
        if len(ob_df) > 120:
            ob_df = ob_df.drop(0)
            return ob_df

