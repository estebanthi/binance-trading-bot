import pandas as pd






def epoch_to_datetime(epoch):
    epoch /= 1000
    return dt.datetime.fromtimestamp(epoch)

import datetime as dt





import ccxt

exchange = ccxt.bitfinex()
data = exchange.fetchOHLCV(symbol="BTC/EUR", timeframe="1d", limit=5000, since=1603466146)


data = format_klines(data)

print(data)