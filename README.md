Here I attempt to build a blockchain which can store the order book date and the recent trades of Bitcoin of the main CEXes.

They are the two aspects of micro-market data who quant traders need.
Such as Binance, OKX, Coinbase, Kraken, Bybit, Gateio and so on.
And contains 7 trading pairs, which are 'BTCUSDT' and 'BTCFDUSD' of Binance, 'BTC-USD' of Coinbase, 'BTC-USDT' of OKX, 'BTCUSDT' of Bybit, 'BTC_USDT' of Gateio, and 'BTC/USD' of Kraken.
This 7 exchanges of Bitcoin trading volume contain more than 99% of the Bitcoin trading of total market.
The Data contains four aspects of Bitcoin trading, which are the sum of 10 bid volume, the sum of 10 ask volume, the sum of buy volume and the sum of sell volume of every 1 second.
With the above 7 trading pairs, this data has 7*4=28 columns. Which are {exchange}_bid_sum, {exchange}_ask_sum, {exchange}_buy_sum, {exchange}_sell_sum.
So this blockchain must adding one block every 1 second.
What proof mechanism does this blockchain require, POS or POW? Or other mechanism else?
