from models.Datafeeds.DatafeedParams import DatafeedParams as DatafeedParams
import datetime as dt
import backtrader as bt
from models.Datafeeds.DatafeedGenerator import DatafeedGenerator as DatafeedGenerator
import warnings
warnings.filterwarnings("ignore")


params = DatafeedParams(mode="PAPER", symbol="BTC/EUR", timedelta=dt.timedelta(hours=100), timeframe=bt.TimeFrame.Minutes,

                        compression=1)

generator = DatafeedGenerator(params)
print(generator.generate_datafeed())