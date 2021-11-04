from models.Strategies.BracketStratSkeleton import BracketStratSkeleton as BracketStratSkeleton
from backtrader.indicators import BollingerBands as BB
from backtrader.indicators import ExponentialMovingAverage as EMA
from models.Strategies.Strategy import Strategy as Strategy
from dataclasses import dataclass


class Core(BracketStratSkeleton):
    params = (
        ('bb_period', 20),
        ('devfactor', 2),
        ('trend_ema_period', 200),
    )

    def __init__(self):
        super().__init__()
        self.bb = BB(period=self.p.bb_period, devfactor=self.p.devfactor)
        self.ema200 = EMA(period=self.p.trend_ema_period)

    def get_long(self):
        if self.ema200[0] < self.datas[0].close[0] < self.bb.bot[0]:
            return True
        return False

    def get_short(self):
        if self.ema200[0] > self.datas[0].close[0] > self.bb.top[0]:
            return True
        return False


@dataclass
class BollingerBandsDivergence(Strategy):

    def __init__(self, logging=Core.params.logging, longs_enabled=Core.params.longs_enabled, shorts_enabled=Core.params.shorts_enabled,
                 stop_loss=Core.params.stop_loss, risk_reward_ratio=Core.params.risk_reward_ratio,
                 bb_period=Core.params.bb_period, devfactor=Core.params.devfactor, trend_ema_period=Core.params.trend_ema_period):
        self.strategy = Core
        self.parameters = locals()
        self.remove_self()
