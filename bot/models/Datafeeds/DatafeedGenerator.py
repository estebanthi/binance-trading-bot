import backtrader as bt
import os
from models.Datafeeds.CustomOHLC import CustomOHLC as CustomOHLC
import yaml
from binance import Client
import pandas as pd
import datetime as dt
from ccxtbt import CCXTStore
import time
from models.MongoDriver import MongoDriver as MongoDriver
from backtrader.feeds.pandafeed import PandasData as PandasData

# Useful to format timeframe and compression
timeframes_mapper = {
    bt.TimeFrame.Minutes: "m",
    bt.TimeFrame.Days: "d",
    bt.TimeFrame.Months: "M",
}


class DatafeedGenerator:
    """ Class to generate datafeed from params """

    def __init__(self, datafeed_params):
        self.p = datafeed_params

        if type(self.p.start_date) == str:
            self.p.start_date = dt.datetime.strptime(self.p.start_date, "%Y/%m/%d %H:%M:%S")
        if type(self.p.end_date) == str:
            self.p.end_date = dt.datetime.strptime(self.p.end_date, "%Y/%m/%d %H:%M:%S")

        if self.p.timedelta:
            self.p.start_date = self.p.end_date - self.p.timedelta

    def generate_datafeed(self):
        datafeed = None
        if self.p.mode == "BACKTEST" or self.p.mode == "OPTIMIZE":
            datafeed = self.generate_backtesting_datafeed()
        else:  # PAPER or REAL
            datafeed = self.generate_live_datafeed()
        return datafeed

    def generate_backtesting_datafeed(self):
        """ Generate datafeed for backtesting purpose """

        with open("config.yml", "r") as file:
            data = yaml.safe_load(file)

        if data["mongo_url"]:
            mongo_driver = MongoDriver()
            mongo_driver.connect()
            if not mongo_driver.get_ticker(self.p.symbol, self.format_timeframe()):
                historical = format_klines(self.extract_klines(), 1).to_dict("records")
                mongo_driver.add_ticker(self.p.symbol, self.format_timeframe(), historical)
            else:
                historical = mongo_driver.get_historical(self.p.symbol, self.format_timeframe())
                if historical[0]["Date"] > self.p.start_date or historical[-1]["Date"] < self.p.end_date:
                    updated_historical = format_klines(self.extract_klines(), 1).to_dict("records")
                    mongo_driver.update_ticker(self.p.symbol, self.format_timeframe(), updated_historical)
            filtered_data = filter_historical(self.p.start_date, self.p.end_date, historical)
            return PandasData(dataname=filtered_data, timeframe=self.p.timeframe, compression=self.p.compression)
        title = self.get_file_title()

        if not os.path.isfile(f"data/datasets/{title}"):
            klines = self.extract_klines()
            klines_formatted = format_klines(klines)
            klines_formatted.to_csv(f"data/datasets/{title}")
        return CustomOHLC(dataname=f"data/datasets/{title}", timeframe=self.p.timeframe, compression=self.p.compression, sessionstart=self.p.start_date)

    def generate_live_datafeed(self):
        """ Explicit """

        with open("config/config.yml") as file:
            data = yaml.safe_load(file)
        key, secret = data["api_key"], data["api_secret"]

        # Broker config
        broker_config = {
            'apiKey': key,
            'secret': secret,
            'nonce': lambda: str(int(time.time() * 1000)),
            'enableRateLimit': True,
        }

        # Getting store
        store = CCXTStore(exchange='binance', currency=None, config=broker_config, retries=5,
                          debug=self.p.debug)

        return store.getdata(dataname=self.p.symbol, name=self.p.symbol, timeframe=self.p.timeframe,
                             fromdate=self.p.start_date, compression=self.p.compression, ohlcv_limit=99999,
                             sessionstart=self.p.start_date)

    def get_file_title(self):
        """ Find the title associated to params """

        start_date_str, end_date_str = self.p.start_date.strftime("%Y-%m-%d"), self.p.end_date.strftime("%Y-%m-%d")
        symbol_str = self.p.symbol.replace("/", "-")
        tf_str = self.format_timeframe()

        return f"{symbol_str}_{start_date_str}_{end_date_str}_{tf_str}.csv"

    def extract_klines(self):
        """ Extract klines from params """

        with open("config.yml") as file:
            data = yaml.safe_load(file)

        # Connection to API
        api_key, api_secret = data["api_key"], data["api_secret"]
        client = Client(api_key, api_secret)

        timeframe = self.format_timeframe()
        start, end = self.p.start_date, self.p.end_date
        symbol = self.p.symbol.replace("/", "")

        return client.get_historical_klines(symbol=symbol, interval=timeframe, start_str=str(start), end_str=str(end))

    def format_timeframe(self):
        """ Format timeframe to Binance API interval format"""
        if self.p.timeframe == bt.TimeFrame.Minutes:
            if self.p.compression == 60:
                return "1h"
            if self.p.compression == 120:
                return "2h"
            if self.p.compression == 240:
                return "4h"
        return f"{self.p.compression}{timeframes_mapper[self.p.timeframe]}"


def format_klines(klines, mode=0):
    # Generate a nice DataFrame from Binance raw data

    columns = 'open_time open high low close volume close_time quote_asset_volume number_of_trades taker_buy_base_asset_volume taker_buy_quote_asset_volume ignore'.split(
        ' ')

    df = pd.DataFrame(klines, columns=columns)
    df = df.astype('float64')
    sub_df = df[['open_time', 'open', 'high', 'low', 'close', 'quote_asset_volume']]

    temp_serie = [epoch_to_datetime(row[1]['open_time']) for row in df.iterrows()]
    sub_df['open_time'] = temp_serie

    sub_df.columns = 'Date, Open, High, Low, Close, Volume'.split(', ')
    if mode:
        return sub_df
    sub_df.set_index('Date', inplace=True)

    return sub_df


def epoch_to_datetime(epoch):
    epoch /= 1000
    return dt.datetime.fromtimestamp(epoch)


def filter_historical(start, end, historical):
    df = pd.DataFrame()
    df = df.from_records(historical)
    after = df[df["Date"] >= start]
    before = df[df["Date"] <= end]
    between = after.merge(before)
    between.set_index(["Date"], inplace=True)
    return between