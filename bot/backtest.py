# Put here your imports
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
from models.Observers.Value import Value as ValueObserver
from models.Timers.StopSession import StopSession as StopSession
from models.TelegramBot.TelegramBot import TelegramBot as TelegramBot
from models.Sizers.PercentSizer import PercentSizer as PercentSizer
from models.Strategies.BracketStrats.BollingerBandsDivergences import \
    BollingerBandsDivergence as BollingerBandsDivergence

# To disable useless warnings
warnings.filterwarnings("ignore")

# Put here your trading components
strategies = [TripleEMA(logging=False, fastestperiod=range(10, 35, 3), middleperiod=range(40, 80, 5),
                        slowestperiod=range(90, 150, 10))]
analyzers = [TradeAnalyzer(), PercentGetter(multiplier=100)]
observers = [ValueObserver()]
sizer = PercentSizer(99)

# You can add a telegram bot if you want
telegram_bot = TelegramBot()

# Instantiate the engine
engine = Engine()

# Configure the engine
config = EngineConfiguration(
    mode="BACKTEST",
    symbol="BTC/EUR",
    start_date="2020/01/01 0:0:0",
    end_date="2021/11/01 0:0:0",
    timeframe=bt.TimeFrame.Days,
    compression=1,
    strategies=strategies,
    analyzers=analyzers,
    stdstats=True,
    observers=observers,
    sizer=sizer,
    telegram_bot=telegram_bot,
    save_results="results.dat"
)
engine.set_configuration(config)

# Run the engine
engine.run()

telegram_bot.send_message("BACKTEST FINISHED")
