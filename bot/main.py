from models.Datafeed.DatafeedParams import DatafeedParams as DatafeedParams
import datetime as dt
import backtrader as bt
from models.Datafeed.DatafeedGenerator import DatafeedGenerator as DatafeedGenerator
import warnings
warnings.filterwarnings("ignore")


params = DatafeedParams(mode="BACKTEST", symbol="BTC/EUR", start_date=dt.datetime.utcnow()-dt.timedelta(hours=10), timeframe=bt.TimeFrame.Minutes,
                        compression=1)

generator = DatafeedGenerator(params)
print(generator.get_file_title())
print(generator.generate_datafeed())