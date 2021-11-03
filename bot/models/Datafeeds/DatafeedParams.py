from dataclasses import dataclass
import datetime as dt
import backtrader as bt


@dataclass
class DatafeedParams:
    """ Class to modelize datafeed options"""
    mode: str
    symbol: str
    timeframe: bt.TimeFrame
    end_date: dt.datetime = dt.datetime.utcnow()
    start_date: dt.datetime = None
    compression: int = 1
    timedelta: dt.timedelta = None
    debug: bool = False