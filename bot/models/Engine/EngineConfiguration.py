from dataclasses import dataclass
from dataclasses import field
import backtrader as bt
import datetime as dt
from models.Strategies.Strategy import Strategy as Strategy
from models.Sizers.Sizer import Sizer as Sizer
from models.Sizers.DefaultSizer import DefaultSizer as DefaultSizer


@dataclass
class EngineConfiguration:
    """ Class to modelize engine options """
    mode: str
    symbol: str
    timeframe: bt.TimeFrame
    strategy: Strategy
    sizer: Sizer = DefaultSizer()
    end_date: dt.datetime or str = dt.datetime.utcnow()
    start_date: dt.datetime or str = None
    compression: int = 1
    timedelta: dt.timedelta = None
    debug: bool = False
    analyzers: list = field(default_factory=list)
    cash: float = 100_000
    commission: float = 0.2
    kwargs: dict = field(default_factory=dict)
    currency: str = None



