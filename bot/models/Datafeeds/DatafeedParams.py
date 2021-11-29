from dataclasses import dataclass
import datetime as dt
import backtrader as bt
import ccxt


@dataclass
class DatafeedParams:
    """
    Class to modelize datafeed configuration


    Params :

        - mode : str
            Datafeed mode (live or backtesting)

        - symbol : str
            Symbol

        - timeframe : bt.TimeFrame
            Timeframe

        - compression : int
            Compression, default is 1

        - end_date : dt.datetime or str (format "YYYY/MM/DD HH:MM:SS")
            End date, default is NOW

        - start_date : dt.datetime or str (format "YYYY/MM/DD HH:MM:SS")
            Start date, default is None

        - timedelta : dt.timedelta
            If you don't want to use start_date, use timedelta (difference between start and end dates),
            default is None

        - debug : bool
            To debug live datafeed, default is False

        - exchange : ccxt.exchange
            Exchange to use to get data
    """

    mode: str
    symbol: str
    timeframe: bt.TimeFrame
    compression: int = 1
    end_date: dt.datetime or str = dt.datetime.utcnow()
    start_date: dt.datetime or str = None
    timedelta: dt.timedelta = None
    debug: bool = False
    exchange: ccxt.bitfinex or ccxt.binance = ccxt.bitfinex()