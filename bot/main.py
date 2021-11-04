from models.Datafeeds.DatafeedParams import DatafeedParams as DatafeedParams
import datetime as dt
import backtrader as bt
from models.Datafeeds.DatafeedGenerator import DatafeedGenerator as DatafeedGenerator
import warnings
from models.Sizers.DefaultSizer import DefaultSizer
from models.Engine.EngineConfiguration import EngineConfiguration as EngineConfiguration
from models.Strategies.Strategy import Strategy as Strategy


warnings.filterwarnings("ignore")


params = DatafeedParams(mode="PAPER", symbol="BTC/EUR", start_date="2021/11/01 0:0:0", timeframe=bt.TimeFrame.Minutes,
                        compression=1)

strategy = Strategy(bt.StrategyBase, {})
config = EngineConfiguration(symbol="BTC/EUR", mode="PAPER", timeframe=bt.TimeFrame.Minutes, strategy=strategy)