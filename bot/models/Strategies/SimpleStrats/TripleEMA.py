from dataclasses import dataclass
from models.Strategies.Strategy import Strategy as Strategy
from models.Strategies.SimpleStratSkeleton import SimpleStratSkeleton as SimpleStratSkeleton
import backtrader as bt
from dataclasses import field


class TripleEMA_strat(SimpleStratSkeleton):
    params = (
        ('fastestperiod', 20),
        ('middleperiod', 50),
        ('slowestperiod', 200),
    )

    def __init__(self):
        super().__init__()
        self.fast = bt.indicators.EMA(self.datas[0], period=self.params.fastestperiod)
        self.middle = bt.indicators.EMA(self.datas[0], period=self.params.middleperiod)
        self.slow = bt.indicators.EMA(self.datas[0], period=self.params.slowestperiod)

    def get_long(self):
        if self.datas[0].close[0] > self.fast[0] > self.middle[0] > self.slow[0]:
            return True
        return False

    def get_short(self):
        if self.datas[0].close[0] < self.fast[0] < self.middle[0] < self.slow[0]:
            return True
        return False

    def close_long(self):
        if self.datas[0].close[0] < self.fast[0]:
            return True
        return False

    def close_short(self):
        if self.datas[0].close[0] > self.fast[0]:
            return True
        return False

@dataclass
class TripleEMA(Strategy):

    def __init__(self, logging=TripleEMA_strat.params.logging, longs_enabled=TripleEMA_strat.params.longs_enabled, shorts_enabled=TripleEMA_strat.params.shorts_enabled,
                 fastestperiod=TripleEMA_strat.params.fastestperiod, middleperiod=TripleEMA_strat.params.middleperiod, slowestperiod=TripleEMA_strat.params.slowestperiod):
        self.strategy = TripleEMA_strat
        self.parameters = locals()
        self.remove_self()





