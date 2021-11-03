import backtrader as bt
import os
from models.Datafeed.CustomOHLC import CustomOHLC as CustomOHLC
import yaml
from binance import Client
import pandas as pd
import datetime as dt

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

    def generate_datafeed(self):
        if self.p.mode == "BACKTEST":
            datafeed = self.generate_backtesting_datafeed()
        return datafeed

    def generate_backtesting_datafeed(self):
        """ Generate datafeed for backtesting purpose """

        title = self.get_file_title()

        if not os.path.isfile(f"data/datasets/{title}"):
            klines = self.extract_klines()
            klines_formatted = format_klines(klines)
            klines_formatted.to_csv(f"data/datasets/{title}")

        return CustomOHLC(dataname=title, timeframe=self.p.timeframe, compression=self.p.compression)

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


def format_klines(klines):
    # Generate a nice DataFrame from Binance raw data

    columns = 'open_time open high low close volume close_time quote_asset_volume number_of_trades taker_buy_base_asset_volume taker_buy_quote_asset_volume ignore'.split(
        ' ')

    df = pd.DataFrame(klines, columns=columns)
    df = df.astype('float64')
    sub_df = df[['open_time', 'open', 'high', 'low', 'close', 'quote_asset_volume']]

    temp_serie = [epoch_to_datetime(row[1]['open_time']) for row in df.iterrows()]
    sub_df['open_time'] = temp_serie

    sub_df.columns = 'Date, Open, High, Low, Close, Volume'.split(', ')
    sub_df.set_index('Date', inplace=True)

    return sub_df


def epoch_to_datetime(epoch):
    epoch /= 1000
    return dt.datetime.fromtimestamp(epoch)
