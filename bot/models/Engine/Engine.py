import backtrader as bt
from models.Engine.EngineConfiguration import EngineConfiguration as EngineConfiguration
from models.Datafeeds.DatafeedGenerator import DatafeedGenerator as DatafeedGenerator
from models.Datafeeds.DatafeedParams import DatafeedParams as DatafeedParams
import yaml
import time
from ccxtbt import CCXTStore


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
        self.cerebro = bt.Cerebro()
        self.configure_broker()

        datafeed = self.generate_datafeed()
        self.cerebro.adddata(datafeed)

        for analyzer in self.config.analyzers:
            self.cerebro.addanalyzer(analyzer.analyzer, **analyzer.parameters)
        self.cerebro.addsizer(self.config.sizer.sizer, **self.config.sizer.parameters)
        if self.config.mode == "BACKTEST":
            self.cerebro.optstrategy(self.config.strategy.strategy, **self.config.strategy.parameters)
        else:
            self.cerebro.addstrategy(self.config.strategy.strategy, **self.config.strategy.parameters)

        if "timeframes" in self.config.strategy.parameters:
            self.resample_datafeed(datafeed)

        if self.config.mode == "BACKTEST":
            return self.cerebro.run(maxcpus=1, optreturn = False, mode=self.config.mode, **self.config.kwargs)
        return self.cerebro.run(mode=self.config.mode, **self.config.kwargs)



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
        if self.config.mode == "BACKTEST":
            self.cerebro.broker.setcash(self.config.cash)
            self.cerebro.broker.setcommission(self.config.commission/100)
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
        for timeframe in self.config.strategy.parameters["timeframes"]:
            self.cerebro.resampledata(datafeed, timeframe=timeframe[0], compression=timeframe[1])

    def plot(self):
        self.cerebro.plot()