from models.Datafeeds.DatafeedParams import DatafeedParams as DatafeedParams
import datetime as dt
import backtrader as bt
from models.Datafeeds.DatafeedGenerator import DatafeedGenerator as DatafeedGenerator
import warnings
from models.Sizers.DefaultSizer import DefaultSizer
from models.Engine.EngineConfiguration import EngineConfiguration as EngineConfiguration
from models.Strategies.Strategy import Strategy as Strategy
from models.Engine.Engine import Engine as Engine

warnings.filterwarnings("ignore")


strategy = Strategy(bt.strategies.MA_CrossOver, {})
engine = Engine()
config = EngineConfiguration(symbol="BTC/EUR", mode="BACKTEST", start_date="2021/10/01 0:0:0", timeframe=bt.TimeFrame.Minutes, compression=240, strategy=strategy)
engine.set_configuration(config)

print(engine.run())

