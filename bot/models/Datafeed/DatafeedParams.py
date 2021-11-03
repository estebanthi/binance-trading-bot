from dataclasses import dataclass
import datetime as dt
import backtrader as bt


@dataclass
class DatafeedParams:
    """ Class to modelize datafeed options"""
    mode: str
    symbol: str
    start_date: dt.datetime
    timeframe: bt.TimeFrame
    end_date: dt.datetime = dt.datetime.utcnow()
    compression: int = 1
    timedelta: dt.timedelta = None
