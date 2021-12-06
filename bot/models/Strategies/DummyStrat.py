from dataclasses import dataclass
from models.Strategies.Strategy import Strategy
import backtrader as bt
from models.Indicators.HeikinAshiRSI import HeikinAshiRSI

class DummyStrat_strat(bt.Strategy):

    def __init__(self):
        self.heikin = HeikinAshiRSI()

    def next(self):
        print(self.heikin.open[0], self.heikin.high[0], self.heikin.low[0], self.heikin.close[0])


@dataclass
class DummyStrat(Strategy):

    def __init__(self):
        self.strategy = DummyStrat_strat
        self.parameters = locals()
        self.remove_self()
