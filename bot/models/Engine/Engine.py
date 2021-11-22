from models.Datafeeds.DatafeedGenerator import DatafeedGenerator as DatafeedGenerator
from models.Datafeeds.DatafeedParams import DatafeedParams as DatafeedParams
from models.Engine.EngineCerebro import EngineCerebro as EngineCerebro
from models.Timers.StopSession import StopSession as StopSession

import backtrader as bt
from ccxtbt import CCXTStore
import pickle
import yaml
import time


def get_secrets(path='config.yml'):
    with open(path, 'r') as file:
        data = yaml.safe_load(file)
        return data['api_key'], data['api_secret']


class Engine:
    """ Core class of the bot. It's the brain. """

    def __init__(self):
        self.config = None

    def set_configuration(self, config):
        """ Set engine's config """
        self.config = config

    def run(self):
        """ Launch the engine """
        self.cerebro = EngineCerebro()
        self.configure_broker()

        datafeed = self.generate_datafeed()
        self.cerebro.adddata(datafeed)

        # Writer
        if self.config.write_to:
            self.cerebro.addwriter(bt.WriterFile, out="data/backtesting_results/" + self.config.write_to)
        # Analyzers
        for analyzer in self.config.analyzers:
            self.cerebro.addanalyzer(analyzer.analyzer, **analyzer.parameters)
        # Observers
        for observer in self.config.observers:
            self.cerebro.addobserver(observer.observer, **observer.parameters)
        # Sizer
        self.cerebro.addsizer(self.config.sizer.sizer, **self.config.sizer.parameters)
        # Timers
        for timer in self.config.timers:
            stop_session = StopSession()
            self.cerebro.add_timer(timername=timer.timername, function=timer.function,
                                   **timer.parameters)

        for strategy in self.config.strategies:
            if self.config.mode == "BACKTEST" or self.config.mode == "OPTIMIZE":
                self.cerebro.optstrategy(strategy.strategy, **strategy.parameters)
            else:
                self.cerebro.addstrategy(strategy.strategy, **strategy.parameters)

        # Check if a resampling is needed, and resample in that case
        self.resample_datafeed(datafeed)

        try:
            if self.config.mode == "BACKTEST":
                results = self.cerebro.run(maxcpus=1, optreturn=False, mode=self.config.mode, tradehistory=True,
                                           stdstats=self.config.stdstats,
                                           telegram_bot=self.config.telegram_bot, symbol=self.config.symbol,
                                           path_to_result=self.config.write_to, **self.config.kwargs)
            elif self.config.mode == "OPTIMIZE":
                results = self.cerebro.run(maxcpus=1, optreturn=True, mode=self.config.mode,
                                           stdstats=self.config.stdstats,
                                           telegram_bot=self.config.telegram_bot, symbol=self.config.symbol,
                                           path_to_result=self.config.write_to, **self.config.kwargs)

            else:
                results = self.cerebro.run(mode=self.config.mode, telegram_bot=self.config.telegram_bot,
                                           stdstats=self.config.stdstats, symbol=self.config.symbol,
                                           path_to_result=self.config.write_to, **self.config.kwargs)

            if self.config.save_results:
                with open(f"data/backtesting_results/{self.config.save_results}", "wb") as file:
                    pickle.dump(results, file)
            return results

        except Exception as e:
            # Catch errors, and wait 5 seconds before retrying
            print(f"Error : {e}\nRetry in 5 seconds")
            time.sleep(5)
            self.run()

    def generate_datafeed(self):
        """ Generate a datafeed corresponding to config """
        datafeed_params = DatafeedParams(mode=self.config.mode, symbol=self.config.symbol,
                                         timeframe=self.config.timeframe,
                                         end_date=self.config.end_date, start_date=self.config.start_date,
                                         compression=self.config.compression, timedelta=self.config.timedelta,
                                         debug=self.config.debug)
        datafeed_generator = DatafeedGenerator(datafeed_params)
        return datafeed_generator.generate_datafeed()

    def configure_broker(self):
        """ Configure cerebro's broker """
        if self.config.mode != "LIVE":
            self.cerebro.broker.setcash(self.config.cash)
            self.cerebro.broker.setcommission(self.config.commission / 100)
        else:  # Generate a broker from the exchange
            key, secret = get_secrets()
            broker_config = {
                'apiKey': key,
                'secret': secret,
                'nonce': lambda: str(int(time.time() * 1000)),
                'enableRateLimit': True,
            }
            store = CCXTStore(exchange='binance', currency=self.config.currency, config=broker_config, retries=5,
                              debug=self.config.debug)
            broker = store.getbroker()
            self.cerebro.setbroker(broker)

    def resample_datafeed(self, datafeed):
        timeframes = []
        for strategy in self.config.strategies:
            if "timeframes" in strategy.parameters:
                for timeframe in strategy.parameters["timeframes"]:
                    timeframes.append(timeframe)

        timeframes = set(timeframes)
        for timeframe in timeframes:
            self.cerebro.resampledata(datafeed, timeframe=timeframe[0], compression=timeframe[1])

    def plot(self):
        self.cerebro.plot(style='candlestick', barup="green")
