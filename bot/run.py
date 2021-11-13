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


# To disable useless warnings
warnings.filterwarnings("ignore")

# Put here your trading components
strategies = [TripleEMA(logging=True)]
analyzers = [TradeAnalyzer(), PercentGetter(multiplier=100)]
observers = [ValueObserver()]
timers = [StopSession(when=dt.time(21), weekdays=[2])]

# You can add a telegram bot if you want
telegram_bot = TelegramBot()

# If you want a written recap, enter here its name
# Default path where is saved the file is in data/backtesting_results
write_to = "recap.txt"

# Instantiate the engine
engine = Engine()

# Configure the engine
config = EngineConfiguration(
    mode="PAPER",
    symbol="BTC/EUR",
    timedelta=dt.timedelta(hours=10),
    timeframe=bt.TimeFrame.Minutes,
    compression=1, strategies=strategies, debug=False, analyzers=analyzers, currency="EUR",
    write_to=write_to, stdstats=True, observers=observers, telegram_bot=telegram_bot
)
engine.set_configuration(config)

# Run the engine
result = engine.run()

# Plot the results
engine.plot()

# Send the results to the bot
telegram_bot.send_file(open(f"data/backtesting_results/{write_to}", "r"))
