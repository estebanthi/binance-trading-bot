# Put here your imports
import backtrader as bt
import warnings
from models.Engine.EngineConfiguration import EngineConfiguration as EngineConfiguration
from models.Strategies.SimpleStrats.TripleEMA import TripleEMA as TripleEMA
from models.Engine.Engine import Engine as Engine
from models.Results.ResultsAnalyzer import ResultsAnalyzer
from models.Analyzers.TradeAnalyzer import TradeAnalyzer as TradeAnalyzer
from models.Strategies.BracketStrats.StochMacdRsi import StochMacdRsi as StochMacdRsi
import datetime as dt
from models.Observers.Value import Value as ValueObserver
from models.Timers.StopSession import StopSession as StopSession
from models.TelegramBot.TelegramBot import TelegramBot as TelegramBot
from models.Sizers.PercentSizer import PercentSizer as PercentSizer
from models.Strategies.BracketStrats.BollingerBandsDivergences import \
    BollingerBandsDivergence as BollingerBandsDivergence
from models.Strategies.BracketStrats.PSAR_EMA import PSAR_EMA as PSAR_EMA
from models.Sizers.FixedSizer import FixedSizer as FixedSizer
from models.Analyzers.AnnualReturn import AnnualReturn
from models.Analyzers.PyFolio import PyFolio
from models.Analyzers.StratQuality import StratQuality
from models.Analyzers.TradeList import TradeList
import ccxt
import backtrader_plotting
from models.Analyzers.FullMetrics import FullMetrics
from models.Strategies.BracketStrats.EMA_Scalping import EMA_Scalping
from models.Strategies.DummyStrat import DummyStrat
from models.Strategies.BracketStrats.HeikinAshiScalp import HeikinAshiScalp

# To disable useless warnings
warnings.filterwarnings("ignore")

# Put here your trading components
strategies = [HeikinAshiScalp(stop_loss=0.5, risk_reward_ratio=1.5, logging=True)]
analyzers = [FullMetrics(), TradeAnalyzer()]
observers = [ValueObserver()]
sizer = PercentSizer(99)

# Instantiate the engine
engine = Engine()

# Configure the engine
config = EngineConfiguration(
    mode="BACKTEST",
    symbol="BTC/EUR",
    start_date="2021/12/03 0:0:0",
    end_date="2021/12/05 0:0:0",
    timeframe=bt.TimeFrame.Minutes,
    compression=1,
    strategies=strategies,
    analyzers=analyzers,
    stdstats=True,
    observers=observers,
    sizer=sizer,
    commission=0.1,
    exchange=ccxt.bitfinex(),
    use_mongo=False,
    use_bokeh=True,
)
engine.set_configuration(config)

# Run the engine
result = engine.run()

# Charting
"""engine.plot()"""

result_analyzer = ResultsAnalyzer(result)

result_analyzer.print_metrics()