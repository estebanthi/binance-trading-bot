# Put here your imports
import backtrader as bt
import warnings
from models.Engine.EngineConfiguration import EngineConfiguration as EngineConfiguration
from models.Strategies.SimpleStrats.TripleEMA import TripleEMA as TripleEMA
from models.Engine.Engine import Engine as Engine
from models.Analyzers.TradeAnalyzer import TradeAnalyzer as TradeAnalyzer
import datetime as dt
from models.Observers.Value import Value as ValueObserver
from models.Timers.StopSession import StopSession as StopSession
from models.TelegramBot.TelegramBot import TelegramBot as TelegramBot
from models.Sizers.PercentSizer import PercentSizer as PercentSizer
import ccxt


# To disable useless warnings
warnings.filterwarnings("ignore")

# Put here your trading components
strategies = [TripleEMA(logging=True, recurring_recap=dt.timedelta(minutes=100))]
analyzers = [TradeAnalyzer()]
observers = [ValueObserver()]
timers = [StopSession(when=dt.time(16))]
sizer = PercentSizer(99)

# You can add a telegram bot if you want
telegram_bot = TelegramBot()

# If you want a written recap, enter here its name
# Default path where is saved the file is data/backtesting_results
write_to = "recap.txt"

# Instantiate the engine and the exchange
engine = Engine()
exchange = ccxt.binance()


# Configure the engine
config = EngineConfiguration(
    mode="PAPER",
    symbol="BTC/EUR",
    timedelta=dt.timedelta(minutes=50),
    timeframe=bt.TimeFrame.Minutes,
    compression=240, strategies=strategies, debug=False, analyzers=analyzers, currency="EUR",
    write_to=write_to, stdstats=True, observers=observers, sizer=sizer, exchange=exchange
)
engine.set_configuration(config)

# Run the engine
result = engine.run()

# Plot the results
engine.plot()

# Send the results to the bot
telegram_bot.send_file(open(f"data/backtesting_results/{write_to}", "r"))
