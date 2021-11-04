from models.Datafeeds.DatafeedParams import DatafeedParams as DatafeedParams
import datetime as dt
import backtrader as bt
from models.Datafeeds.DatafeedGenerator import DatafeedGenerator as DatafeedGenerator
import warnings
from models.Sizers.DefaultSizer import DefaultSizer
from models.Engine.EngineConfiguration import EngineConfiguration as EngineConfiguration
from models.Strategies.Strategy import Strategy as Strategy
from models.Engine.Engine import Engine as Engine
from models.Analyzers.ResultAnalyzer import ResultAnalyzer as ResultAnalyzer
from models.Analyzers.TradeAnalyzer import TradeAnalyzer as TradeAnalyzer

warnings.filterwarnings("ignore")


strategy = Strategy(bt.strategies.MA_CrossOver, {})
analyzers = [TradeAnalyzer()]
engine = Engine()
config = EngineConfiguration(symbol="BTC/EUR", mode="BACKTEST", start_date="2021/1/01 0:0:0", timeframe=bt.TimeFrame.Minutes,
                             compression=60, strategy=strategy,debug=True, analyzers=analyzers)
engine.set_configuration(config)

result = engine.run()

result_analyzer = ResultAnalyzer(result)
print(result_analyzer.get_pnls())


