# Put here your imports
import backtrader as bt
import warnings

import numpy as np

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
from models.Strategies.BracketStrats.EMA_Scalping import EMA_Scalping
import ccxt

# To disable useless warnings
warnings.filterwarnings("ignore")

# Put here your trading components
strategies = [EMA_Scalping(stop_loss=np.linspace(0.1, 0.5, 10), risk_reward_ratio=np.linspace(1.5, 3, 10))]
analyzers = [TradeAnalyzer()]
observers = [ValueObserver()]
sizer = PercentSizer(99)

# You can add a telegram bot if you want
telegram_bot = TelegramBot()

# Instantiate the engine
engine = Engine()

# Configure the engine
config = EngineConfiguration(
    mode="OPTIMIZE",
    symbol="BNB/BTC",
    start_date="2021/10/01 0:0:0",
    end_date="2021/11/10 0:0:0",
    timeframe=bt.TimeFrame.Minutes,
    compression=1,
    strategies=strategies,
    analyzers=analyzers,
    stdstats=True,
    observers=observers,
    sizer=sizer,
    telegram_bot=telegram_bot,
    save_results="multistrat.dat",
    commission=0.075,
    use_mongo=False,
    exchange=ccxt.binance(),
)
engine.set_configuration(config)

# Run the engine
engine.run()

# Notify
telegram_bot.send_message("OPTIMIZATION FINISHED")
