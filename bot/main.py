import backtrader as bt
import warnings
from models.Engine.EngineConfiguration import EngineConfiguration as EngineConfiguration
from models.Strategies.SimpleStrats.TripleEMA import TripleEMA as TripleEMA
from models.Engine.Engine import Engine as Engine
from models.Analyzers.ResultAnalyzer import ResultAnalyzer as ResultAnalyzer
from models.Analyzers.TradeAnalyzer import TradeAnalyzer as TradeAnalyzer

warnings.filterwarnings("ignore")


strategy = TripleEMA(logging=True, slowestperiod=200)
analyzers = [TradeAnalyzer()]

engine = Engine()
config = EngineConfiguration(symbol="BTC/EUR", mode="BACKTEST", start_date="2021/10/01 0:0:0", timeframe=bt.TimeFrame.Minutes,
                             compression=60, strategy=strategy,debug=True, analyzers=analyzers)
engine.set_configuration(config)

result = engine.run()
engine.plot()

result_analyzer = ResultAnalyzer(result)
print(result_analyzer.get_pnls())