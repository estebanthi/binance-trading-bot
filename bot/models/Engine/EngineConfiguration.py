from dataclasses import dataclass
from dataclasses import field
import backtrader as bt
import datetime as dt
from models.Sizers.Sizer import Sizer as Sizer
from models.Sizers.DefaultSizer import DefaultSizer as DefaultSizer
from models.TelegramBot.TelegramBot import TelegramBot as TelegramBot
import ccxt


@dataclass
class EngineConfiguration:
    """ Class to modelize engine configuration """
    mode: str  # Engine mode (BACKTEST, OPTIMIZE, PAPER, LIVE)
    symbol: str  # Symbol
    timeframe: bt.TimeFrame  # Timeframe
    sizer: Sizer = DefaultSizer()  # Sizer
    end_date: dt.datetime or str = dt.datetime.utcnow()  # End date
    start_date: dt.datetime or str = None  # Start date
    compression: int = 1  # Compression
    timedelta: dt.timedelta = None  # Timedelta if you don't want to use a start date
    debug: bool = False  # If you want to debug datafeed
    analyzers: list = field(default_factory=list)  # Analyzers list
    cash: float = 100_000  # Cash for simulation
    commission: float = 0.2  # Broker's commission
    kwargs: dict = field(default_factory=dict)  # Kwargs for cerebro.run
    currency: str = None  # Currency you are using to pass orders
    write_to: str = None  # Path you want to write results
    stdstats: bool = True  # backtrader's reference
    observers: list = field(default_factory=list)  # Observers list
    timers: list = field(default_factory=list)  # Timers list
    strategies: list = field(default_factory=list)  # Strategies list
    telegram_bot: TelegramBot = None  # TelegramBot
    save_results: str = None  # Results filename if you want to save
    exchange: ccxt.bitfinex or ccxt.binance = ccxt.bitfinex()  # Exchange to use

