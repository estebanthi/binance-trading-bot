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
import ccxt

# Useful to format timeframe and compression
timeframes_mapper = {
    bt.TimeFrame.Minutes: "m",
    bt.TimeFrame.Days: "d",
    bt.TimeFrame.Months: "M",
}


class DatafeedGenerator:
    """
    Class to generate datafeed from params
    Check DatafeedParams to learn more about it

    """

    def __init__(self, datafeed_params):
        self.p = datafeed_params

        if type(self.p.start_date) == str:
            self.p.start_date = dt.datetime.strptime(self.p.start_date, "%Y/%m/%d %H:%M:%S")
        if type(self.p.end_date) == str:
            self.p.end_date = dt.datetime.strptime(self.p.end_date, "%Y/%m/%d %H:%M:%S")

        if self.p.timedelta:
            self.p.start_date = self.p.end_date - self.p.timedelta

    def generate_datafeed(self):
        return self.generate_backtesting_datafeed() if (self.p.mode == "BACKTEST" or self.p.mode == "OPTIMIZE") \
            else self.generate_live_datafeed()

    def generate_backtesting_datafeed(self):
        """
        Generate datafeed for backtesting purpose

        """

        with open("config.yml", "r") as file:
            data = yaml.safe_load(file)

        if data["mongo_url"]:  # If MongoDB is used
            mongo_driver = MongoDriver()
            mongo_driver.connect()
            if not mongo_driver.get_ticker(self.p.symbol, self.format_timeframe()):
                # Ticker not in database, we add it
                historical = format_klines(self.extract_klines()).to_dict("records")
                mongo_driver.add_ticker(self.p.symbol, self.format_timeframe(), historical)
            else:
                historical = mongo_driver.get_historical(self.p.symbol, self.format_timeframe())
                if historical[0]["Date"] > self.p.start_date or historical[-1]["Date"] < self.p.end_date:
                    # Dates no corresponding, we update historical
                    updated_historical = format_klines(self.extract_klines()).to_dict("records")
                    mongo_driver.update_ticker(self.p.symbol, self.format_timeframe(), updated_historical)
            # Filter with dates
            filtered_data = filter_historical(self.p.start_date, self.p.end_date, historical)
            return PandasData(dataname=filtered_data, timeframe=self.p.timeframe, compression=self.p.compression)

        # If we use local storage
        title = self.get_file_title()
        if not os.path.isfile(f"data/datasets/{title}"):
            klines = self.extract_klines()
            klines_formatted = format_klines(klines)
            filtered_data = filter_historical(self.p.start_date, self.p.end_date, klines_formatted)
            filtered_data.to_csv(f"data/datasets/{title}")
        return CustomOHLC(dataname=f"data/datasets/{title}", timeframe=self.p.timeframe, compression=self.p.compression,
                          sessionstart=self.p.start_date)

    def generate_live_datafeed(self):
        """
        Explicit

        """

        with open("config.yml") as file:
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
        """
        Find the title associated to params

        """

        start_date_str, end_date_str = self.p.start_date.strftime("%Y-%m-%d"), self.p.end_date.strftime("%Y-%m-%d")
        symbol_str = self.p.symbol.replace("/", "-")
        tf_str = self.format_timeframe()

        return f"{symbol_str}_{start_date_str}_{end_date_str}_{tf_str}.csv"

    def extract_klines(self):
        """
        Extract klines corresponding to params

        """
        exchange = self.p.exchange
        timestamp = int(dt.datetime.timestamp(self.p.start_date)*1000)
        data = exchange.fetch_ohlcv(self.p.symbol, timeframe=self.format_timeframe(), since=timestamp, limit=10000)
        while data[-1][0] < dt.datetime.timestamp(self.p.end_date)*1000:
            data2 = exchange.fetch_ohlcv(self.p.symbol, timeframe=self.format_timeframe(), since=data[-1][0], limit=10000)
            for i in range(len(data2)):
                if i !=0:
                    data.append(data2[i])
        for i in range(len(data)):
            data[i] = tuple(data[i])
        return data

    def format_timeframe(self):
        """
        Format timeframe to Binance API interval format

        """
        if self.p.timeframe == bt.TimeFrame.Minutes:
            if self.p.compression == 60:
                return "1h"
            if self.p.compression == 120:
                return "2h"
            if self.p.compression == 240:
                return "4h"
        return f"{self.p.compression}{timeframes_mapper[self.p.timeframe]}"


def format_klines(klines):
    """
    Generate a nice DataFrame from Binance raw data

    """

    columns = 'Date Open High Low Close Volume'.split(
        ' ')

    df = pd.DataFrame(klines, columns=columns)
    df = df.astype('float64')

    df.loc[:, "Date"] = df.loc[:, "Date"].apply(epoch_to_datetime)
    return df


def epoch_to_datetime(epoch):
    epoch /= 1000
    return dt.datetime.fromtimestamp(epoch)


def filter_historical(start, end, historical):
    """
    Filter a dataframe with start and end dates

    """
    df = pd.DataFrame()
    df = df.from_records(historical)
    after = df[df["Date"] >= start]
    before = df[df["Date"] <= end]
    between = after.merge(before)
    between.set_index(["Date"], inplace=True)
    return between
