import backtrader as bt
import warnings
from models.Engine.EngineConfiguration import EngineConfiguration as EngineConfiguration
from models.Strategies.SimpleStrats.TripleEMA import TripleEMA as TripleEMA
from models.Engine.Engine import Engine as Engine
from models.Analyzers.ResultAnalyzer import ResultAnalyzer as ResultAnalyzer
from models.Analyzers.TradeAnalyzer import TradeAnalyzer as TradeAnalyzer
from models.Analyzers.PercentGetter import PercentGetter as PercentGetter
from models.Strategies.BracketStrats.StochMacdRsi import StochMacdRsi as StochMacdRsi
import datetime as dt

warnings.filterwarnings("ignore")


strategy = StochMacdRsi()
analyzers = [TradeAnalyzer(), PercentGetter(multiplier=100)]

engine = Engine()
config = EngineConfiguration(symbol="BTC/EUR", mode="PAPER", timedelta=dt.timedelta(days=10), timeframe=bt.TimeFrame.Minutes,
                             compression=60, strategy=strategy,debug=True, analyzers=analyzers, currency="EUR"
                             )
engine.set_configuration(config)

result = engine.run()

engine.plot()

result_analyzer = ResultAnalyzer(result)
print(result_analyzer.get_pnls())

print(result[0][0].analyzers.percent_getter.get_analysis())