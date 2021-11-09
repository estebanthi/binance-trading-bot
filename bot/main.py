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

warnings.filterwarnings("ignore")

strategies = [StochMacdRsi(logging=True, recurring_recap=dt.timedelta(minutes=240))]
analyzers = [TradeAnalyzer(), PercentGetter(multiplier=100)]
stop_session = StopSession(when=dt.time(21), weekdays=[2])
timers = [stop_session]

bot = TelegramBot()

engine = Engine()
write_to = "recap.txt"
config = EngineConfiguration(symbol="BTC/EUR", mode="PAPER", timedelta=dt.timedelta(hours=3),
                             timeframe=bt.TimeFrame.Minutes,
                             compression=1, strategies=strategies, debug=False, analyzers=analyzers, currency="EUR",
                             write_to=write_to, stdstats=False, observers=[ValueObserver()],
                             stop_timer_timedelta=dt.timedelta(minutes=5), timers=timers,
                             telegram_bot=bot
                             )
engine.set_configuration(config)

result = engine.run()

bot.send_file(open(f"data/backtesting_results/{write_to}", "r"))
